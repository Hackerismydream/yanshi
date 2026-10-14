# 偃师 Logo v2 设计记录

## 上轮问题

已查看 `images/logo-a.png`、`logo-b.png`、`logo-c.png` 原图。

- A：横竖构件太平淡，第一眼像字母或普通 T 形；榫卯关系依赖解释，缺少鲜明轮廓。
- B：头、肩、胸、关节和底座堆叠，躯干像服装人台；细节在小尺寸竞争，不能直接作为小图标。
- C：舟形加圆孔更像帽子或眼睛，墨斗器物本身难认，放线也不足以纠正误读。

## 外部 Skill 与方法

按要求只执行 `git clone --depth 1`，克隆至 `vendor-skills/`；未运行仓库脚本，未全局安装，未改 Codex 配置，未读取密钥文件。该目录是追加要求对新增文件范围的明确例外。

选用 [anthropics/skills](https://github.com/anthropics/skills) 的 [`skills/canvas-design/SKILL.md`](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md)，本地位于 `vendor-skills/anthropics-skills/skills/canvas-design/SKILL.md`。借鉴流程：先写视觉理念，再落实形状、空间、颜色和构图；文化意象嵌入结构；成图后第二遍检查，优先精炼现有形状而非添加装饰。检查清单为单一主体、边界留白、主体分离、视觉平衡、缩小后的轮廓。其海报文字、密集图案、字体下载建议不适用于本任务，以用户的无字、极简、内置图像生成要求为准。

另克隆并阅读 [adrianpunk/Punk-Skill](https://github.com/adrianpunk/Punk-Skill) 的 `skills/punk-cover/SKILL.md`，它主要针对带标题的社交封面，本轮不选用，也未套用其封面风格。

出图使用内置 imagegen，每个方案一次独立调用。英文 prompt 统一包含用途、主体隐喻、几何构成、构图、准确色值、缩略图约束和排除项，完整保存于下文。选择四个无字方向，不采用「偃」字或 Y 字形，因此不涉及错字保留。

## 视觉理念：机关留白

东方感来自有辨识度的结构：回纹、发髻侧脸、斗拱和提线控制。每张只用一种文化线索，避免把古典符号堆成装饰。

科技感来自构件的精确接合和粗壮的负形孔洞。形状首先是一枚可辨识的符号，文化解释是第二层；不靠电路纹、发光或材质完成科技感。

空间优先服务缩小使用。主体居中，外轮廓紧凑，关键间隙尽量达到原图 90px；在 16px 下仍约有 1.4px，在 64px 下约有 5.6px。实际成图仍须视觉复查，prompt 不等于验收结果。

颜色遵循 DESIGN.md 第 2 节：浅底 #F8FAFB 配 #365667；深底 #101A23 配 #8EAFBF。第四案允许少量 #E28B80 连接点；任何红色细节都不能承担核心辨识功能。反复检查轮廓与间距，不用细节数量代替设计完成度。

## 四个方案与实际英文 Prompt

### 1. 回纹机关印

```text
Use case: logo-brand. Asset: one standalone logo symbol for Yanshi, an engineering agent workflow inspired by an ancient Chinese automaton maker. Output one 1024 x 1024 PNG, square. Flat vector-like geometric design with perfectly solid fills, crisp edges, carefully balanced negative space, no texture, shading, gradients, glow, shadows, perspective or 3D. Center a single compact emblem in the central 68% of the canvas, with generous clear margins. It must remain recognizable at 16-64 pixels: use very few bold masses, essential strokes and gaps at least 90 pixels at full resolution. No typography, no Chinese characters, no Latin letters, no numbers, no pseudo-writing, no watermark, no captions, no border around the canvas, no mockup, no variants or contact sheet. Background solid #F8FAFB. Symbol solid #365667. Create an abstract Chinese seal emblem made from two bold interlocking squared spiral hooks, reminiscent of ancient Chinese meander ornament and precision-fitted mechanical parts. The hooks form one almost-square, open-ended rotational knot, with one large clear central negative-space socket. Only two simple thick angular hooks, not a maze, not a character, not a letter. The cultural identity must come from the meander seal silhouette, the technology from precise modular interlocking. No red accent needed.
```

### 2. 机关人侧脸

```text
Use case: logo-brand. Asset: one standalone logo symbol for Yanshi, an engineering agent workflow inspired by an ancient Chinese automaton maker. Output one 1024 x 1024 PNG, square. Flat vector-like geometric design with perfectly solid fills, crisp edges, carefully balanced negative space, no texture, shading, gradients, glow, shadows, perspective or 3D. Center a single compact emblem in the central 68% of the canvas, with generous clear margins. It must remain recognizable at 16-64 pixels: use very few bold masses, essential strokes and gaps at least 90 pixels at full resolution. No typography, no Chinese characters, no Latin letters, no numbers, no pseudo-writing, no watermark, no captions, no border around the canvas, no mockup, no variants or contact sheet. Background solid #101A23. Symbol solid #8EAFBF. Create a minimal right-facing side-profile head of an ancient Chinese wooden automaton. One strong compact head silhouette with a small integrated angular topknot, a clearly stepped forehead, nose and chin contour, and a single large square negative-space joint socket at the temple. No torso or shoulders. No separate eye, mouth line, ear detail, neck decoration or helmet. The topknot and carved profile suggest a Chinese artisan-made figure; the square temple socket suggests a precisely engineered mechanism. Calm and restrained, not a warrior, not a cute robot.
```

### 3. 斗拱齿轮

```text
Use case: logo-brand. Asset: one standalone logo symbol for Yanshi, an engineering agent workflow inspired by an ancient Chinese automaton maker. Output one 1024 x 1024 PNG, square. Flat vector-like geometric design with perfectly solid fills, crisp edges, carefully balanced negative space, no texture, shading, gradients, glow, shadows, perspective or 3D. Center a single compact emblem in the central 68% of the canvas, with generous clear margins. It must remain recognizable at 16-64 pixels: use very few bold masses, essential strokes and gaps at least 90 pixels at full resolution. No typography, no Chinese characters, no Latin letters, no numbers, no pseudo-writing, no watermark, no captions, no border around the canvas, no mockup, no variants or contact sheet. Background solid #F8FAFB. Symbol solid #365667. Fuse a Chinese dougong bracket and a mechanical cog into ONE compact silhouette. The upper half is a broad stepped bracket with two boldly rising squared ends and one lower tier, instantly recalling traditional Chinese timber architecture without drawing a roof. The lower half is a thick semicircular mechanical hub with exactly three broad square teeth pointing left-down, down and right-down. A single large square negative-space hub sits at the center. Keep the bracket and cog fully integrated, not two stacked icons. No fine gear teeth, no roof illustration, no decorative linework.
```

### 4. 悬丝控制架

```text
Use case: logo-brand. Asset: one standalone logo symbol for Yanshi, an engineering agent workflow inspired by an ancient Chinese automaton maker. Output one 1024 x 1024 PNG, square. Flat vector-like geometric design with perfectly solid fills, crisp edges, carefully balanced negative space, no texture, shading, gradients, glow, shadows, perspective or 3D. Center a single compact emblem in the central 68% of the canvas, with generous clear margins. It must remain recognizable at 16-64 pixels: use very few bold masses, essential strokes and gaps at least 90 pixels at full resolution. No typography, no Chinese characters, no Latin letters, no numbers, no pseudo-writing, no watermark, no captions, no border around the canvas, no mockup, no variants or contact sheet. Background solid #101A23. Symbol solid #8EAFBF, with a single #E28B80 square joint smaller than 1% of canvas area. Create an extremely minimal Chinese marionette control emblem: a wide shallow angular arch with subtly raised ends, inspired by a traditional wooden puppet controller. From its two ends descend exactly two short thick vertical suspension links to a single broad angular U-shaped cradle below; within that cradle sits one bold square puppet head. The upper arch, hanging links and suspended square form one coherent compact control mechanism, not a humanoid body. Use broad open spaces; the tiny red joint is optional and never necessary to recognize the symbol. No thin strings, no complete puppet, no cross or T shape, no lantern tassels.
```

## 自查、取舍与推荐

| 方案 | 概念与实际效果 | 64px 实看 | 16px 补充实看 | 自评 |
| --- | --- | --- | --- | --- |
| 1 回纹机关印 | 两个粗折钩组成旋转回纹，借印章的方整感表达构件协作；无文字 | 折钩和中央留白清楚，轮廓紧凑 | 两个钩仍可分开，内部弯折略糊 | 最简洁，但容易被理解成通用链接/迷宫图标，东方感不如人物直接 |
| 2 机关人侧脸 | 发髻、鼻梁、下颌组成朝右侧脸，太阳穴方孔是机械关节 | 发髻、侧脸与方孔均清楚，没有人台式躯干 | 人头轮廓和方孔仍可见，发髻分隔缩成细缝 | 推荐。与偃师的造人故事联系最直接，几何方孔带来机械感；发髻仍可能被看成小帽，是保留的解释风险 |
| 3 斗拱齿轮 | 上半部阶梯式斗拱和下半部三齿轮共用方孔 | 方孔与三齿完整；左右上翘端清楚 | 外轮廓与方孔仍成立，斗拱台阶弱化 | 结构稳、机械感强，但也可能像牛角或工具徽章，东方辨识依赖对斗拱的熟悉程度 |
| 4 悬丝控制架 | 斜杆、两根粗悬挂连接和方头肩梁表达受控机关 | 重生成后连接清楚，头部与肩梁可辨 | 大结构仍在，头肩细缝弱化 | 已改进初稿的灯笼感，但仍可能像吊架/门架，东方感最弱，不推荐作主标 |

以上是对实际缩略图的设计自查，不是用户识别测试；“图形可辨”不等于陌生人一定认出具体器物。四案均无可见文字、字母、水印或乱码。未使用字形印章，因此没有「偃」字校对失败的问题。

第一至第三案未发现需要重生成的明显主体跑偏。第四案初稿出现两个朱砂连接点且外形像灯笼，按要求重生成一次；最终采用第二次结果。下列为第四案实际重生成的完整英文 prompt（上文仍保留第一轮 prompt 供追溯）：

```text
Use case: logo-brand. Asset: one standalone logo symbol for Yanshi, an engineering agent workflow inspired by an ancient Chinese automaton maker. Output one 1024 x 1024 PNG, square. Flat vector-like geometric design with perfectly solid fills, crisp edges, carefully balanced negative space, no texture, shading, gradients, glow, shadows, perspective or 3D. Center a single compact emblem in the central 68% of the canvas, with generous clear margins. It must remain recognizable at 16-64 pixels: use very few bold masses, essential strokes and gaps at least 90 pixels at full resolution. No typography, no Chinese characters, no Latin letters, no numbers, no pseudo-writing, no watermark, no captions, no border around the canvas, no mockup, no variants or contact sheet. Background solid #101A23. Symbol solid #8EAFBF, with a single #E28B80 square joint smaller than 1% of canvas area. Create an extremely minimal Chinese marionette control emblem: a wide shallow angular arch with subtly raised ends, inspired by a traditional wooden puppet controller. From its two ends descend exactly two short thick vertical suspension links to a single broad angular U-shaped cradle below; within that cradle sits one bold square puppet head. The upper arch, hanging links and suspended square form one coherent compact control mechanism, not a humanoid body. Use broad open spaces; the tiny red joint is optional and never necessary to recognize the symbol. No thin strings, no complete puppet, no cross or T shape, no lantern tassels.
Refinement after thumbnail review: replace the lantern-like enclosed U-shaped cradle with a clearly suspended angular puppet shoulder beam, open underneath, and a square head above that beam. Keep two suspension links very thick, at least 100px at 1024px scale. The upper controller must be a short diagonal wooden lever rather than a roof. Use ONLY #8EAFBF on #101A23, no red accents at all. Exactly four bold elements: diagonal controller, two thick suspension links, and the connected head-and-shoulder mass. No body, no arms, no enclosing frame. Entire symbol must look like a controllable marionette rather than a lantern or shopping bag. Absolutely uniform flat fills.
```

### 推荐使用第二案

推荐 `images/logo-v2-2.png`。它把上轮 B 的完整人台减到头部轮廓，保留故事性，同时让方形关节孔承担科技语义。64px 下不需要胸口、肩膀或多处关节解释身份；16px 下也能保留侧脸和孔洞。第一案可作为更抽象的备用方向，第三案适合偏工程工具的品牌气质，第四案只保留为探索。

### 交付与验证记录

- 最终四张主图：`images/logo-v2-1.png` 至 `logo-v2-4.png`，均为 1024×1024 PNG。
- 按要求使用 macOS `sips` 生成四张 `logo-v2-N-64.png`，逐张实际查看。
- 另用 `sips` 生成四张 `logo-v2-N-16.png` 并查看，用于补充验证 16px 边界。
- 内置工具返回的方形原始图片经 `sips -s format png -z 1024 1024` 统一到交付尺寸，再从交付主图生成缩略图；没有用代码重画 Logo。
- Prompt 使用 DESIGN.md 第 2 节色值；图像生成与缩放会带来细微色差和抗锯齿，未声称每个像素都严格等于指定色值。成品为扁平几何构图，未加入材质、立体效果或光效。
- 文件尺寸和 PNG 格式以 `sips -g pixelWidth -g pixelHeight -g format` 复核。尝试用 Pillow 辅助统计颜色时本机未安装该模块，没有安装依赖；改用系统 sips 完成文件规格检查，未完成精确颜色直方图检查。
- Anthropic 克隆版本：`dbd4588f9e1033efb41dad4bef2f7947c8993d44`；Punk 克隆版本：`c9ad7a3745e07060c50270141efed418a0cd04d6`。
- 本次仅新增本笔记、`design/images/logo-v2-*` 和追加授权的两个 `vendor-skills/` 克隆目录；未改旧图、DESIGN.md、README、项目代码或全局配置，未执行外部 Skill 的任何脚本。
