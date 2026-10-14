"""Temporary mechanical fixtures only; not examples of author incidents."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import setup as sut

PACKAGE=Path(__file__).resolve().parents[1]

def files(root):
    return {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file() and not p.is_symlink()}

class SetupTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='yanshi-setup-test-')
        self.root=Path(self.temp.name)
        self.project=self.root/'project';self.project.mkdir()
        self.home=self.root/'home';self.home.mkdir()
    def tearDown(self):
        self.temp.cleanup()
    def test_project_preview_has_no_writes(self):
        before=files(self.project)
        self.assertEqual(len(sut.prepare_project(self.project)),3)
        self.assertEqual(files(self.project),before)
    def test_project_preserves_old_text(self):
        old=b'# Existing\r\nKeep every byte.\r\n'
        for name in ('AGENTS.md','CLAUDE.md'):
            (self.project/name).write_bytes(old)
        sut.apply_project(self.project,sut.prepare_project(self.project))
        for name in ('AGENTS.md','CLAUDE.md'):
            self.assertTrue((self.project/name).read_bytes().startswith(old))
        self.assertIn(b'@.yanshi/INDEX.md',(self.project/'CLAUDE.md').read_bytes())
    def test_project_idempotent(self):
        sut.apply_project(self.project,sut.prepare_project(self.project))
        before=files(self.project)
        self.assertEqual(sut.prepare_project(self.project),[])
        sut.apply_project(self.project,[])
        self.assertEqual(before,files(self.project))
    def test_override_is_used(self):
        (self.project/'AGENTS.override.md').write_text('Override instructions\n')
        (self.project/'AGENTS.md').write_text('Do not change this\n')
        sut.apply_project(self.project,sut.prepare_project(self.project))
        self.assertIn(sut.BEGIN,(self.project/'AGENTS.override.md').read_bytes())
        self.assertEqual((self.project/'AGENTS.md').read_text(),'Do not change this\n')
    def test_empty_override_falls_back(self):
        (self.project/'AGENTS.override.md').write_text(' \n')
        plan=sut.prepare_project(self.project)
        self.assertIn('AGENTS.md',[c.path.name for c in plan])
    def test_existing_index_not_overwritten(self):
        p=self.project/'.yanshi/INDEX.md';p.parent.mkdir();p.write_text('Existing project index\n')
        sut.apply_project(self.project,sut.prepare_project(self.project))
        self.assertEqual(p.read_text(),'Existing project index\n')
    def test_damaged_managed_block_refuses_all(self):
        (self.project/'CLAUDE.md').write_bytes(sut.BEGIN+b'\nunfinished')
        before=files(self.project)
        with self.assertRaises(ValueError):sut.prepare_project(self.project)
        self.assertEqual(before,files(self.project))
    def test_project_symlink_refused(self):
        (self.project/'.yanshi').symlink_to(self.root/'outside',target_is_directory=True)
        with self.assertRaises(ValueError):sut.prepare_project(self.project)
        self.assertFalse((self.root/'outside').exists())
    def test_concurrent_edit_refused_before_writes(self):
        plan=sut.prepare_project(self.project)
        (self.project/'CLAUDE.md').write_text('Concurrent edit\n')
        with self.assertRaises(ValueError):sut.apply_project(self.project,plan)
        self.assertFalse((self.project/'.yanshi').exists())
    def test_project_rollback_after_io_error(self):
        original=sut.atomic_write
        count=0
        def fail_second(path,data):
            nonlocal count
            count+=1
            if count==2:raise OSError('injected failure')
            return original(path,data)
        with patch.object(sut,'atomic_write',side_effect=fail_second):
            with self.assertRaises(OSError):sut.apply_project(self.project,sut.prepare_project(self.project))
        self.assertEqual(files(self.project),{})
    def test_install_preview_has_no_writes(self):
        plan=sut.prepare_install(PACKAGE,self.home,'both')
        self.assertEqual(len(plan),24)
        self.assertEqual(files(self.home),{})
    def test_both_installs_byte_identical(self):
        plan=sut.prepare_install(PACKAGE,self.home,'both')
        sut.apply_install(self.home,plan)
        for source,dest in plan:self.assertEqual(files(source),files(dest))
    def test_repeat_install_refused(self):
        sut.apply_install(self.home,sut.prepare_install(PACKAGE,self.home,'both'))
        before=files(self.home)
        with self.assertRaises(ValueError):sut.prepare_install(PACKAGE,self.home,'both')
        self.assertEqual(before,files(self.home))
    def test_late_host_collision_prevents_early_copy(self):
        dest=self.home/'.claude/skills/yanshi-boundary';dest.mkdir(parents=True)
        with self.assertRaises(ValueError):sut.prepare_install(PACKAGE,self.home,'both')
        self.assertFalse((self.home/'.agents').exists())
    def test_dangling_symlink_refused(self):
        dest=self.home/'.claude/skills/yanshi';dest.parent.mkdir(parents=True)
        dest.symlink_to(self.home/'missing',target_is_directory=True)
        with self.assertRaises(ValueError):sut.prepare_install(PACKAGE,self.home,'both')
        self.assertFalse((self.home/'.agents').exists())
    def test_install_failure_rolls_back(self):
        plan=sut.prepare_install(PACKAGE,self.home,'both')
        with patch.object(sut.shutil,'copytree',side_effect=OSError('injected copy failure')):
            with self.assertRaises(OSError):sut.apply_install(self.home,plan)
        self.assertFalse(any(dest.exists() for _,dest in plan))
    def test_preview_cli_reports_no_writes(self):
        result=subprocess.run([sys.executable,str(PACKAGE/'scripts/setup.py'),'project','--project',str(self.project)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('PREVIEW ONLY',result.stdout)
        self.assertEqual(files(self.project),{})
    @unittest.skipUnless(shutil.which('git'),'git is unavailable')
    def test_nested_repository_root_refused(self):
        subprocess.run(['git','init','-q',str(self.project)],check=True)
        nested=self.project/'nested';nested.mkdir()
        with self.assertRaises(ValueError):sut.prepare_project(nested)

if __name__=='__main__':unittest.main()
