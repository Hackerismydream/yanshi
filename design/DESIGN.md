# yanshi（偃师）视觉方案

## 1. 设计理念

**以榫卯为骨，以电路为线。** 偃师的机关人是受人指挥、可以拆装的工具，正好对应 yanshi 按任务复杂度取用工作流的方式。画面强调工匠的尺度、结构和连接关系，传达「日常开发中大家真正在用的 Skill」的实用感。

定稿组合：**机关人侧脸 Logo + 无字工坊场景封面 + 浅色工作流正文配图**。中国风来自榫头、木构关节、墨斗放线与工笔轮廓；科技感来自精确几何、局部发光和稀疏网格。单幅画面只保留一个主要文化意象，不堆砌器物。

正文信息图继承参考图的信息层级、低饱和蓝灰、线性图标与红色修复回路。X 长文与通用社交封面默认无字，用具体场景补充标题；正文信息图保留流程密度。本文依据 [README](../README.md) 与 [Skill 定义](../skills/yanshi/SKILL.md)；参考封面按任务提供的文字描述提炼，不作像素级复刻。

## 2. 配色

### 深色版：墨蓝工坊

用于 README 头图、社交封面和深色背景上的品牌标识。

| 角色 | 色值 | 用途 |
| --- | --- | --- |
| 主色：青灰 | `#8EAFBF` | Logo、机关人主轮廓、正常路径；微光也只用此色 |
| 辅色：钢蓝 | `#526C7A` | 次级结构线、榫卯剖面、节点描边，不作小字 |
| 强调色：朱砂 | `#E28B80` | 一个关键连接点；流程图中只用于问题与修复 |
| 背景：墨蓝 | `#101A23` | 主画布，大面积纯色 |
| 表面：深蓝灰 | `#1B2B37` | 必要的节点填充、局部结构面 |
| 文字：月白 | `#EDF2F4` | 品牌名、主标题、节点名 |
| 次级文字：雾灰 | `#B3C2CA` | 副标题、说明、步骤辅助文字 |

### 浅色版：纸上蓝图

用于流程信息图、浅色文档和印刷预览。纸色接近白，不做泛黄古籍。

| 角色 | 色值 | 用途 |
| --- | --- | --- |
| 主色：墨青 | `#365667` | Logo、箭头、结构描边、图标 |
| 辅色：浅蓝 | `#E5EEF3` | 节点填充、分区淡底 |
| 强调色：朱砂 | `#A8443A` | 问题回路箭头与对应标签 |
| 背景：素纸 | `#F8FAFB` | 主画布，可替换为纯白 `#FFFFFF` |
| 文字：墨黑 | `#172B36` | 标题、正文、节点名 |
| 次级文字：蓝灰 | `#526875` | 副标题与辅助说明 |
| 边线：淡蓝灰 | `#B5C7D2` | 分区虚线和非语义网格，不用于正文 |

背景占画面约 75% 以上，朱砂面积不超过 3%。蓝灰微光属于主色明度变化，不再增加荧光青、紫或金色。网格仅在插画区域出现，建议 32–48 px 间距、8%–12% 不透明度，文字背后保持干净。正文对比度验收目标为 4.5:1，关键图形为 3:1；半透明元素需按合成后的颜色复核，装饰网格不承担信息。

## 3. 字体建议

| 场景 | 字体与字重 | 选择理由 | 许可来源 |
| --- | --- | --- | --- |
| 品牌中文「偃师」 | 思源宋体 CN，SemiBold / Bold | 横细竖粗带来工匠与典籍气息；仅用于大字号品牌字，不把流程图变成古风海报 | [SIL OFL 1.1](https://raw.githubusercontent.com/adobe-fonts/source-han-serif/master/LICENSE.txt) |
| 中文功能标题、流程节点 | 思源黑体 CN，Bold | 延续参考图粗黑标题，长节点名仍清楚利落 | [SIL OFL 1.1](https://raw.githubusercontent.com/adobe-fonts/source-han-sans/master/LICENSE.txt) |
| 中文正文、辅助说明 | 思源黑体 CN，Regular / Medium | 密集信息中保持稳定字面和阅读节奏 | 同上 |
| 英文品牌、英文与代码词、步骤数字 | JetBrains Mono，Medium / Regular | 与开发工具语境一致；数字对齐，英文词不做装饰性变形 | [SIL OFL 1.1](https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/OFL.txt) |
| 可选的文化注记 | 霞鹜文楷，Regular | 只用于一行短注的手写温度；不用于节点、正文或小尺寸 Logo | [SIL OFL 1.1](https://raw.githubusercontent.com/lxgw/LxgwWenKai/main/OFL.txt) |

上述字体允许商业使用。随可编辑素材分发字体文件时保留对应版权与许可；修改字体时遵守保留字体名称条件，不将字体文件单独售卖。字体许可不等于项目或视觉资产的发布许可，本文不替项目选择许可证。

默认每张图只用思源黑体和 JetBrains Mono；出现品牌中文大字时再加入思源宋体。霞鹜文楷仅作替代选项，不与三者同时叠用。中文使用简体 CN 字形，逐字确认「偃师」；数字编号统一用 0–8。英文与中文混排时按视觉基线对齐，不用机械放大字距填满一行。

## 4. Logo 方案

### 定稿

正式 Logo 为 **机关人侧脸方案（logo-v2-2）原版**，源文件：[images/logo-v2-2.png](images/logo-v2-2.png)，1024 × 1024 px。所有版本从此图确定性处理得到，保持原画布、留白、轮廓及中央方孔；不重新生图，不裁切、不描边、不增删结构。

成品统一存放于 [../assets/logo/](../assets/logo/)：

| 文件 | 尺寸（px） | 用途与配色 |
| --- | --- | --- |
| `yanshi-logo-dark.png` | 1024 × 1024 | 深色底原版，直接复制源文件；标称背景 `#101A23`、图形 `#8EAFBF`，保留原图轻微色差 |
| `yanshi-logo-transparent.png` | 1024 × 1024 | 深色背景使用，透明底、青灰 `#8EAFBF` 图形 |
| `yanshi-logo-transparent-ink.png` | 1024 × 1024 | 浅色背景使用，透明底、墨青 `#365667` 图形 |
| `yanshi-logo-light.png` | 1024 × 1024 | 固定素纸背景 `#F8FAFB`、墨青 `#365667` 图形 |
| 上述两种透明版及浅色版，文件名加 `-512`、`-128`、`-32` | 512 × 512、128 × 128、32 × 32 | 各尺寸均由 1024 原始 alpha 经 LANCZOS 缩放，再按固定前景色合成，避免深色污染 |
| `favicon.ico` | 内含 16 × 16、32 × 32、48 × 48 | 浅底墨青版；逐尺寸对比后，中央方孔与侧脸轮廓更易辨认 |
| `preview-on-white.png`、`preview-on-black.png` | 各 1024 × 1024 | 青灰透明版分别合成到纯白、纯黑背景，用于检查抗锯齿边缘 |

**透明处理**：按 RGB 欧氏颜色距离计算 `alpha = clamp((distance(pixel, #101A23) - n) / (distance(#8EAFBF, #101A23) - n), 0, 1)`。`n = 5.830952`，取自原图顶部 180 行空白区的最大背景色距离，用连续线性过渡消除轻微底色噪声，不以二值硬阈值切边。透明图所有像素的 RGB 统一为对应前景色，仅由 alpha 保留覆盖率，从而去除边缘背景污染。白底、黑底合成预览已目视检查，未见深色脏边。

**最小使用尺寸**：一般展示不小于 32 × 32 px；README 用 128 px 资源显示为 120 px，并通过 `<picture>` 适配深浅主题。16 px 仅供 favicon，细节辨识有限；不为小尺寸另改形状。所有尺寸保持源图留白，不拉伸。

**未采用方案**：原 A / B / C，以及 v2 的 `logo-v2-1`、`logo-v2-3`、`logo-v2-4` 均未采用。以下方案、提示词及其小尺寸简化规则仅作历史记录，不适用于定稿。

### A. 榫卯之合（未采用）

- **概念**：两个构件各自简单，连接后成为可工作的整体，表达按需组合与清楚的任务边界。
- **构成**：两块垂直交接的几何木构，一处矩形榫头与对应凹槽；中央负形形成清楚的连接口。不写字母，也不强行把复杂汉字嵌入标志。朱砂仅点在接合处，大尺寸允许使用，小尺寸删除。
- **适用尺寸**：主标识 48–256 px；24–32 px 使用单色两构件；16 px favicon 手工整理为一个粗实轮廓和一个至少 2 px 的凹口，最细实体不少于 2 px。删除木纹、电路线、发光与朱砂点，保留接合特征。
- **留白**：四周至少为图形宽度的 1/4。图形独立成立，中文和英文名称均后期排版。

```text
Create a minimalist symbol for an open-source everyday agent development skill inspired by traditional Chinese mortise-and-tenon joinery. Square canvas, 1:1, 1024 x 1024 pixels, transparent background with real alpha, no checkerboard. Center two bold orthogonal geometric members joined by one rectangular tenon and one matching socket. Use a deliberate open notch and strong negative space so the connection remains legible as a tiny icon. Flat vector-like construction, crisp edges, balanced optical weight, no perspective. Main color #365667, with one optional tiny #A8443A inset at the joint. The silhouette must work in one color. Keep the symbol inside the central 64 percent of the canvas. No text, no letters, no Chinese characters, no numbers, no watermark, no gradients, no glow, no wood grain, no decorative frame, no dragons, no lanterns, no gold.
```

### B. 方寸机关人（未采用）

- **概念**：有明确关节、可被调度的机关人，呼应偃师故事中的造物；神态中性，避免机械战士与可爱聊天机器人。
- **构成**：一个方圆之间的头部、梁式双肩、胸口榫槽；双臂由两段构件连接，不画完整手指。胸口一处朱砂定位点代表当前动作，不作眼睛。只保留上半身。
- **适用尺寸**：完整标识用于 96 px 以上；32–64 px 仅保留头、肩、胸口缺口，去掉手臂关节。16 px 不使用完整机关人，改用同方案的单色头肩轮廓，去掉五官与胸口细节；若辨识不足，统一采用 A 的 favicon。
- **取舍**：故事性更强，但细节多，不如 A 适合仓库头像与工具栏。更适合作为封面插画母题。

```text
Design a restrained emblem of a traditional Chinese articulated wooden automaton, represented only by a head, shoulder beam, and upper torso. Square canvas, 1:1, 1024 x 1024 pixels, solid background #101A23. Use bold flat geometric shapes in #8EAFBF with clearly separated negative spaces. Suggest mortise-and-tenon joints at the shoulders and one rectangular socket in the chest. A single small #E28B80 inset may mark the chest joint. Calm, neutral, useful workshop instrument, subtle human silhouette, no expressive face. Front view, centered, generous margin, strong monochrome silhouette. No fine grain, no tiny gears, no strings, no realistic human skin, no armor, no cute robot eyes, no text, no letters, no numbers, no watermark, no company branding, no model names, no gold.
```

### C. 墨斗放线（未采用）

- **概念**：工匠先定准线再开工，对应需求边界与业务契约先于验证结果。
- **构成**：侧视墨斗抽象为短而厚的舟形盒体，内留一个线轴圆孔；一根直线从盒体伸出，终点为方形定位块。线条末端只转折一次，兼具工具放线与电路走线的联想。
- **适用尺寸**：48 px 以上保留放线；24–32 px 缩短线段、放大定位块；16 px 只留实心盒体和 3 px 负形圆孔，不依赖细长线识别。作为横向签名图标更合适。
- **取舍**：器物感最独特，但非熟悉木工的读者可能无法认出墨斗，需与「yanshi 偃师」字标一起首次出现。

```text
Create a compact graphic emblem inspired by a traditional Chinese carpenter's ink-line reel, a mo dou. Square canvas, 1:1, 1024 x 1024 pixels, transparent background with real alpha. Draw a short boat-shaped ink box as one solid geometric silhouette in #365667, with one large circular negative-space spool opening. Extend a short straight ink line to the right, ending at one square anchor in #A8443A; allow only one right-angle bend to subtly suggest a circuit trace. Keep the complete emblem inside the central 68 percent of the canvas. Flat vector-like design, sturdy proportions, clean negative space, no perspective, no distressed texture. No text, no letters, no numbers, no watermark, no decorative seal, no gold, no dragons, no lanterns.
```

## 封面原则

以下原则适用于本文所有封面类 prompt。X 长文与通用社交封面的生成结果和最终交付图都默认无字；README 头图、小红书/抖音带字变体按各自明确的例外执行。

1. **封面与标题是一个整体。** 标题已显示在封面旁边，封面不再重复标题、关键词、卖点或数字，也不额外放品牌字标。不能把「先生成无字底图，再补标题」当成无字封面。
2. **图片提供标题之外的东西。** 用具体的人、场景和感受把抽象概念变成画面，与标题接力，不逐字图解标题。偃师主题通过工匠与机关人共同工作的动作，呈现专注、协作和工具正在被使用的状态。
3. **工具类内容展示使用瞬间。** 教程、工作流优先呈现真实场景中的工具状态，例如终端里 Codex 正在处理任务，或「输入 → 处理 → 输出」刚刚发生的那一刻。封面以人的操作、终端面板状态和产物变化承接这件事，不画流程箭头或步骤列表。插画中的终端依据实际使用时的窗口布局与操作关系提炼，用无字几何块呈现活动区域，不生成伪代码，也不冒充真实产品截图；具体命令与运行证据放在正文截图中。
4. **固定风格，变化场景。** 默认持续使用 A 中国风科技：墨蓝背景、青灰主轮廓、钢蓝次级线、单处朱砂连接点，沿用第 2 节色值。固定平视或轻微侧视的中景、克制的工笔轮廓、清楚的榫卯关节；每张只选一个工作动作，以一处终端亮面聚焦，周围保留大块暗部。人物关系、线条密度、镜头距离和留白比例保持一致，每篇只更换操作与产物。B 黑白蚀刻版画作为另一套可持续使用的备选系列，保留同样的构图与工坊母题，用黑白排线替代彩色线描；同一系列不逐篇随机切换画风。
5. **文字只用于减少猜测和查找。** 只有读者确实需要图中文字才能辨认内容时才加字。README 头图可用项目名与定位帮助识别项目；小红书/抖音封面可用精确标题区分内容，按 5.4 节后期排版。这些例外不回流到 X 默认封面。
6. **备选风格采用无字黑白复古蚀刻版画与复古未来主义。** 参考意象是一张 2.5:1 横幅：黑底白线的夜色海面与地平线落日，中央立着空画框，框内是更明亮的日落海景。全画面只靠排线和点刻表现明暗，以「框中之景」形成极简、强隐喻和克制的高级感。偃师版本沿用这种明暗与嵌套画面手法，把亮框变为机关人胸口的终端，场景改为工匠与机关人在工坊对坐；也可表现木制机关人手持刻刀，在竹简和终端之间工作。保留古老工艺与未来工具并置的张力，不照搬海景或增加装饰文字。

## 5. README 头图、社交封面与正文配图

### 共同制作规则

所有封面类 prompt 均遵守「封面原则」，并明确要求 `no text, no letters, no watermark`。X 长文与通用社交封面生成后不再叠加文字；只有 README 头图、小红书/抖音带字变体及正文信息图采用「生成无字底图，后期排版文字」。这些场景的中文、数字、箭头和 Logo 字标按各自精确清单，用可编辑图层制作，避免错字和伪代码。尺寸是最终交付画布要求；若生成工具不能直接输出指定尺寸，按相同比例或保留安全区生成，再裁切排版，不拉伸主体。

以下是制作规格，不代表本次已生成或验证了图片。所有图中不出现公司信息、模型名、模型版本名、虚构指标、作者签名或水印。

### 5.1 README 头图：工坊中的可控机关

**尺寸**：1280 × 640 px，2:1，深色版。

**README 场景例外**：头图承担项目识别与定位，可保留项目名和以下说明文字。此版式仅用于 README，不裁切为 X 长文或通用社交封面。

**构图**：左侧 56% 用于名称和定位，右侧 36% 为机关人半身结构图，中间留出约 8% 呼吸区。外边距 64 px。主体由少量梁、销和榫槽构成，姿态微侧，肩关节的一条结构线自然延伸为电路。一个较大的定位节点连接两个较小的工作节点，表达人的指挥；不画满屏提线，避免失控傀儡感。右侧局部网格与淡工笔线描并存，木质仅以少量刻线暗示，不渲染厚重木纹。

**文字精确内容与排版**：

| 位置 | 精确内容 | 建议字号 |
| --- | --- | --- |
| 左上名称 | `yanshi 偃师` | 英文 64 px；中文 68 px |
| 左侧主句，固定两行 | `日常开发中` / `大家真正在用的 Skill` | 思源黑体 Bold，38 px，行高 1.3 |
| 左侧辅助句，固定两行 | `按任务复杂度编排 Agent` / `从需求对齐到可验证的交付` | 24 px，行高 1.5 |
| 左下短句 | `简单任务直接做，复杂任务按需加步骤` | 22 px |

表中的 `/` 只表示换行，不绘入图片。文字最大宽度 650 px，整体垂直居中；定稿机关人侧脸 Logo 可放在名称左侧，但不挤占标题宽度。README 缩放至约 640 px 宽时，主句仍需能读清。更窄屏幕由图片替代文本承接信息，建议替代文本：`yanshi 偃师：按任务复杂度编排 Agent，从需求对齐到可验证的交付。`

```text
Create a text-free editorial illustration background for an open-source agent development skill. Final composition 1280 x 640 pixels, aspect ratio 2:1. Use a flat deep ink-blue background #101A23. Keep the left 56 percent completely quiet and empty for typography, with a 64-pixel outer safe margin. Place a carefully constructed half-body Chinese wooden automaton in the right 36 percent, using sparse gongbi-inspired precision linework and geometric mortise-and-tenon joints. The figure is a useful crafted instrument, calm and slightly turned, with no dramatic face. Draw primary contours in muted blue-gray #8EAFBF and secondary structure in #526C7A. Let one joinery edge continue into a precise circuit trace linking one larger control node to two small work nodes. Use one tiny muted vermilion #E28B80 joint accent. Add a barely visible drafting grid only behind the figure and extremely restrained blue-gray edge glow. Airy, intelligent, practical, crafted, understated. no text, no letters, no watermark, no pseudo-writing, no numbers, no logos, no company branding, no model names, no neon spectacle, no gold, no dragons, no lanterns, no palace scenery, no dense gears, no photorealistic hands.
```

### 5.2 X 长文与通用社交封面：工坊里的工作瞬间

**默认最终成图无字**：不加标题、项目名、关键词、卖点、数字或 Logo 字标，不预留标题栏。画面展示偃师工坊与终端/Agent 工作瞬间，读者从人物动作、工具和产物之间的关系理解场景。

| 用途 | 比例与交付尺寸 | 构图规则 |
| --- | --- | --- |
| X 长文横幅 | 2.5:1，2000 × 800 px | 工匠、机关人与终端横向展开，桌面连接三者；四边安全区至少 80 px |
| 16:9 社交分享版 | 16:9，1200 × 675 px | 拉近人物与桌面关系，增加垂直空间；四边安全区至少 60 px |

两个比例分别构图，不机械裁切或拉伸。下列 A、B prompt 默认输出 2.5:1；制作 16:9 时，将首句画布规格替换为 `Canvas 1200 x 675 pixels, aspect ratio 16:9.`，并将安全区改为 60 px，重排人物距离，保留完整的操作动作与终端亮面。缩至 360 px 宽检查时，应能认出人物在使用工具，以及输入、处理和产物的空间关系，无需读字。

#### A. 中国风科技（默认）

偃师坐在工坊桌旁，手正操作终端键盘；木制机关人与他隔桌相对，把刚加工好的榫卯构件递回桌面。终端仍显示任务处理中面板的无字布局，形成「人输入、工具处理、产物出现」的同一瞬间。用真实操作姿态承接工作流主题，保留等待结果时的专注感。沿用墨蓝工坊配色，终端微光只用青灰，朱砂只点一个工作关节，不加漂浮节点和流程箭头。

```text
Canvas 2000 x 800 pixels, aspect ratio 2.5:1. Create a finished wordless editorial cover showing one concrete working moment in Yan Shi's quiet Chinese artisan workshop. At a shared workbench, a human craftsperson is operating a physical terminal keyboard while an articulated wooden automaton seated opposite returns a freshly fitted mortise-and-tenon component. The terminal is still active, capturing the moment between an input, ongoing agent processing, and a tangible output. Base the posture and terminal panel arrangement on an observed real tool-use reference; simplify the screen into non-linguistic geometric activity blocks, without simulated code or invented product UI claims. Eye-level medium view, restrained gongbi-inspired contours, precise wooden joints, sparse material detail. Use #101A23 for the large quiet background, #8EAFBF for primary contours and the single terminal light source, #526C7A for secondary lines, and one tiny #E28B80 accent at the working joint. Keep the figures, operating hand, screen and returned component at least 80 pixels from every edge. Compose across the full width with generous dark breathing room, no reserved headline column. Convey focused everyday work and calm cooperation. no text, no letters, no watermark. No numbers, pseudo-writing, readable code, labels, logos, company branding, model names, title overlays, infographic arrows, floating workflow nodes, neon colors, gold, dragons, lanterns, armor, or dense gears.
```

#### B. 黑白蚀刻版画 / 复古未来主义（备选）

偃师与机关人在暗处对坐，机关人胸口嵌着一块明亮的终端屏，呼应参考意象的「框中之景」。偃师一只手停在与胸口终端相连的桌面键盘上，机关人持刻刀，正在将终端里的处理状态落实为竹片上的榫槽。终端仅用无字面板和活动块表达运行状态，竹片不刻文字。黑底白线，所有明暗由疏密排线与点刻形成，不使用彩色强调、平滑渐变或数码光晕。此方向是封面的单色风格例外，不改变品牌配色、字体或 Logo。

```text
Canvas 2000 x 800 pixels, aspect ratio 2.5:1. Create a finished wordless retro-futurist editorial cover as an intricate black-and-white engraving / etching. In a dark Chinese workshop, the artisan Yan Shi sits face to face with an articulated wooden automaton across a workbench. His hand rests on a physical keyboard connected to a luminous rectangular terminal inset into the automaton's chest. The automaton holds a small carving knife and is cutting a joinery slot into a blank bamboo slat while the terminal remains active. Show a plausible tool-use moment with input, processing and physical output coexisting in one scene. Use non-linguistic geometric panels on the screen, with no readable code. Treat the bright chest screen as a picture within the picture, borrowing the visual logic of an empty frame holding a brighter sunset above a dark sea, but depict only the workshop. Pure black ground and fine white engraved lines; create every tonal transition and the impression of screen light through cross-hatching and stippling only. Eye-level medium view, spare composition, one bright focal frame, broad quiet dark areas, restrained silhouettes, precise wooden joints, strong visual metaphor. Keep the operating gesture and terminal at least 80 pixels from all edges. No headline area. no text, no letters, no watermark. No numbers, pseudo-writing, labels, logos, company branding, model names, calligraphy, infographic arrows, colored accents, smooth gradients, digital bloom, decorative borders, or steampunk gear clutter.
```

### 5.3 正文配图 / README 内插图：按需选择的 0–8 步

**用途**：保留流程图信息，用于文章正文解释或 README 内插图，不作为封面，也不以缩略版嵌入封面。

**尺寸**：2000 × 1000 px，2:1，浅色版。延续参考图的横向流程、两块圆角虚线分区与闭环箭头。选择比参考略高的画布，为九个步骤及跳过语义留出空间；不把密集图缩成社交封面的副图。

**版式与精确文字**：

- 顶部居中主标题：`我的日常 Agent 开发工作流`，64 px 粗黑体；下方副标题：`yanshi 偃师 · 0–8 步按复杂度取用`，28 px。
- 第一分区标题：`① 判断复杂度，按需对齐、设计与审查`。区域建议 x=60、y=170、宽 1880、高 250 px。左到右排列步骤 0、1、2；步骤 1 澄清目标、边界与验收，步骤 2 先设计方案，再做对抗性审查，审查通过后将两步结论统一定稿为 Spec 或 CONTEXT.md。步骤 2 内预留审查退回方案设计的小回路，不增加步骤编号；步骤 0 下方另放短路径条：`简单任务：直接实现 → 自测`。该条由步骤 0 单独引出，不经过步骤 1、2。
- 第二分区标题：`② 每个可验收的小增量，按需循环`。区域建议 x=60、y=450、宽 1880、高 410 px。上排左到右放步骤 3、4、5、6，下排右侧放步骤 7、左侧放步骤 8，以折返箭头连接；下排中央留给修复回路与说明。
- 分区外底部两行结论：`先判断复杂度，再选需要的步骤，不必走完全部流程。` 与 `端到端测试：预期来自业务契约，工具只提供证据。`，26 px。

各节点精确文字如下。编号独立置于圆圈，不改变顺序；主标题 28 px Bold，副标题 22 px Regular。长标题可按词组换行，不缩小字号。

| 编号 | 节点主标题 | 副标题 | 线性图标 |
| --- | --- | --- | --- |
| 0 | 判断复杂度 | 选择够轻的路径 | 规矩与分岔线 |
| 1 | 需求对齐 | 澄清目标、边界、验收 | 对话气泡与竹简式文档 |
| 2 | 方案设计与审查 | 设计 → 对抗性审查 → 定稿 Spec | 灯泡与刻刀 |
| 3 | 拆分与执行 | 按需拆分、并行与集成 | 榫卯拼接与终端 |
| 4 | 实现者自测 | 测试、修复、做减法 | 烧瓶 |
| 5 | 交叉对抗性审查 | 不同 Agent 或新会话 | 两个错位对话框 |
| 6 | 端到端测试 | 契约预期与运行证据 | 终端与放大镜 |
| 7 | 人工 Review | 核对验收与高风险路径 | 人像与清单 |
| 8 | 沉淀与做减法 | 复用有效流程，删除冗余 | 刻刀与收纳后的构件 |

**连接语义**：

1. 步骤 0 是选路起点；已有可信判断时沿用，不画成每轮强制重做。复杂路径从 0 经 1、2 通向第二分区，线旁标 `按需扩展`。
2. 主路径用蓝灰实线箭头。第一、第二分区内分别标 `按需选用，可跳过已有结论或不适用环节`，让实线表示阅读次序，不表示九步强制关卡。步骤 2 内从 `对抗性审查` 以朱砂虚线小回路返回 `设计`，标签为 `审查不过，回到方案设计`；审查通过后才沿实线进入 `定稿 Spec`，统一沉淀需求对齐与方案审查结论（也可使用 CONTEXT.md）。该小回路不接入实现修复回路，且不得穿过节点文字。第二分区入口标 `简单任务跳过拆分，直接实现`。
3. 5、6、7 发现问题时，以朱砂虚线汇入下排中央的 `发现问题 → 实现者修复 → 重新验证`，再回到步骤 4；修复后按受影响范围继续验证，不能暗示只跑自测就已完成端到端验证。回路线不得穿过任何节点文字。
4. 7 完成当前增量后，可沿外侧蓝灰回线回到 3，标签为 `有下一增量时`；本次结束时按需进入 8。用条件标签区分继续开发与收尾沉淀，不让步骤 8 看起来每轮必做。
5. 角落图例精确写 `实线：所选路径`、`朱砂虚线：问题修复`。分区虚线是无箭头的浅蓝灰边框，避免与修复线混淆。

**质感**：节点浅蓝填充、墨青 2–3 px 描边，圆角 12–16 px；图标以 3 px 工笔式线描绘制，只有图标轮廓允许极轻手绘起伏，箭头和文字保持规整。竹简只借纵向分栏或短绑线，不画写满字的卷轴。不加立体投影、光晕或暗底电路，信息图优先清楚。

**英文 prompt**：仅生成同一风格的无字底板。节点、图标、连线和上文全部文字后期制作，以确保准确流程；不让模型猜测箭头关系。

```text
Create a very restrained text-free background plate for a Chinese workflow infographic. Canvas 2000 x 1000 pixels, aspect ratio 2:1, near-white background #F8FAFB. Leave a clear title zone above y=160. Draw exactly two large empty rounded rectangular section outlines using subtle blue-gray #B5C7D2 dashed strokes: the first at x=60, y=170, width=1880, height=250; the second at x=60, y=450, width=1880, height=410. Leave the entire interiors empty for precise typography, workflow nodes, icons, and arrows to be added later. Reserve the bottom 120 pixels for two concluding lines. Suggest traditional Chinese workshop drafting only through a few extremely faint orthogonal joinery construction marks outside the panels near the far corners. Flat, quiet, clean, low-saturation blue-gray, no visible paper grain behind content. Do not draw any text, letters, numbers, labels, icons, nodes, arrows, logos, seals, watermarks, company branding, or model names. No red ornament, gold, dragons, lanterns, gradients, glow, or shadows.
```

若生成底板的边框位置不准确，后期按坐标重画；不为保留生成结果牺牲节点间距。信息图按原尺寸与 1000 px 宽各检查一次，手机端允许点开原图阅读，不承诺九步内容在信息流缩略图中全部可读。

### 5.4 小红书 / 抖音带字封面变体

**尺寸**：1080 × 1440 px，3:4。此变体是帮助读者在信息流中区分内容的带字例外，不用于 X 长文。沿用 A 的配色、工笔轮廓和工坊动作，改为竖向构图；上方约 30% 为干净文字区，下方约 60% 为工匠、机关人与终端，其余为间隔。四边安全区至少 72 px，标题不压人物与屏幕。

**精确文字**：只保留以下内容，建议在生成无字底图后排版，不让模型生成中文。

| 位置 | 精确内容 | 建议排版 |
| --- | --- | --- |
| 上方第一行 | `我的日常` | 思源黑体 Bold，80 px |
| 上方第二行 | `Agent 开发工作流` | 思源黑体 Bold，80 px；英文用 JetBrains Mono 对齐基线 |
| 标题下短句 | `简单任务直接做，复杂任务按需加步骤` | 思源黑体 Medium，36 px，可在逗号后换行 |

不再追加数字角标、卖点标签或重复品牌名。文字采用月白，辅助句用雾灰，沿用既有字体规范；缩略图中优先确保两行标题可读。

```text
Create a wordless background plate for a Chinese social-platform cover that will receive exact editorial typography later. Canvas 1080 x 1440 pixels, aspect ratio 3:4. Reserve the upper 30 percent as clean flat #101A23 negative space and place the working scene in the lower 60 percent. Show an artisan operating a terminal keyboard across a workbench from a wooden automaton returning a newly fitted joinery component, with the terminal still active. Use realistic operating gestures and abstract non-linguistic screen activity blocks, no simulated code. Eye-level medium view, precise gongbi-inspired outlines, restrained mortise-and-tenon joints. Use #8EAFBF for contours and terminal light, #526C7A for secondary structure, and one tiny #E28B80 working-joint accent. Keep all important elements inside a 72-pixel safe margin. Preserve the calm, focused workshop style of the horizontal cover series. no text, no letters, no watermark. No numbers, pseudo-writing, readable code, logos, company branding, model names, infographic arrows, neon spectacle, gold, dragons, or lanterns. Typography will be added afterward, not generated in this image.
```

## 6. 使用规范与禁忌

- **同一套骨架**：Logo、插画与图标共用直角接合、局部圆角和开放凹口；工笔线只用于器物轮廓，不把整张图画成水墨山水。
- **标识先看轮廓**：品牌名统一 `yanshi 偃师`，不换成难认的篆字。定稿 Logo 按第 4 节使用，检查深浅背景与实际展示尺寸；缩小只做 LANCZOS 重采样，不删改细节，不靠发光维持辨识。
- **颜色承担固定含义**：中国风科技封面朱砂只点一个连接位置；黑白蚀刻封面仅用黑白；信息图朱砂只标问题修复，不另加红印章或红色标题。正文信息图无论颜色如何变化，都用箭头方向和标签表达流程；封面不承担流程说明。
- **清晰优先**：文字不压网格、电路线或木纹。仅在 README 头图、带字变体与正文信息图中排版文字，按各自清单核对「偃师」、标题、0–8 编号与节点名称；不使用模型生成的中文或伪代码。不得加入公司信息、模型名或版本名。
- **避免俗套与重量感**：不用红金配色、龙凤、灯笼、宫殿、祥云边框、满屏齿轮、赛博霓虹和写实机械战甲；不画九道关卡、九枚强制勾选框或全自动无人驾驶式叙事。
- **发布前核对**：X 封面先检查最终图确实无字、场景与标题互补、工具处于使用状态；再按各目标尺寸检查安全区与裁切。带字例外检查文字对比，正文信息图检查图标和回路；深浅背景分别检查透明标识。流程图必须能看出简单任务只需实现与自测，并保留业务契约决定端到端预期的原则。

Logo 已按第 4 节从定稿原图导出并检查；本文其余封面、插画与信息图规格不因此视为已交付或已验收。
