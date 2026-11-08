# 海报与PPT的案例转译

按当前难点阅读相关行。2026-11-08核对原始案例说明、文档和所列仓库文件；“做法”是本技能的独立转译，不是来源作者制定的通用规则。没有把客户图、全套模板、第三方指令和后端纳入本技能。

| 实际来源 | 值得采用的能力 | 放在哪里 | 采用边界 |
|---|---|---|---|
| [Pentagram：MoMA](https://www.pentagram.com/work/moma) | 一个焦点图像与稳定字图系统，系列中允许尺度/裁切变化 | 海报构图与跨画幅 | 保留项目自己的身份，不复制MoMA标识与字库 |
| [Pentagram：Poster House](https://www.pentagram.com/work/poster-house) | 识别元素作为可变化的画面边界 | 系列海报与章节视觉 | 边界是可选组织，不强制所有画面套框 |
| [Studio Dumbar：D&AD 2022](https://studiodumbar.com/work/d-ad-2022) | 同一视觉语言随消息、场合改变表现强度 | 海报系列与PPT角色强度 | 动态文字转为静态时挑清晰帧，不堆重复字 |
| [UDL：China TDC 2021](https://u-d-l.com/work/china-tdc-2021-2/) | 从中文主题和公众观看语境形成视觉身份 | 中文字图与主题主张 | 不把原活动题材、字形和内容继承给新项目 |
| [Duarte](https://www.duarte.com/blog/4-presentation-design-principles-to-live-by/) | 语义色贯穿，重要处强化视觉对比 | PPT成套参数与重点页 | 不固定成两种颜色或固定字号 |
| [Assertion–Evidence](https://writing.engr.psu.edu/assertion_evidence_EA.html) | 一句话主张由视觉证据支持，次要细节转入讲解 | 技术/论证型PPT页面 | 适合时采用，不抹掉法规、模板或阅读材料所需内容 |
| [Slidev](https://sli.dev/builtin/layouts.html)、[Quarto](https://quarto.org/docs/presentations/revealjs/themes)与[Marpit](https://marpit.marp.app/image-syntax) | 布局、主题与图片适配分开；功能页面家族可复用 | PPT模块、留白和裁切 | 借方法，不要求用这些引擎生成PPT |
| [PPT-Design-Skill实际入口](https://github.com/sunchaokun/PPT-Design-Skill/blob/main/skill/SKILL.md) | 观众与目标先行、成套参数、缩略图与最终页检查、局部与方向问题分别修正 | PPT组织、实际使用尺寸检查 | 不照搬初始化工具、强制确认次数和最终用户验收门槛 |
| [Codex Slides模板](https://github.com/nexu-io/codex-slides/blob/master/src/lib/templates.ts)与[社区目录](https://github.com/nexu-io/codex-slides/blob/master/src/lib/community.ts) | 内容类别、视觉参数、密度与来源身份分别记录 | 共享路由与风格元数据 | 目录混含结构与外观，先拆分；其整页图片PPTX不等于原生可编辑页面 |
| [PosterMELD](https://github.com/Shannon4Science/PosterMELD) | 先核容量，来源支撑内容，针对失败区域修正 | 信息型海报容量与可编辑排版 | 学术海报不是所有宣传海报的默认布局；未运行上游基准 |
| [原始提示词项目](https://github.com/Nihilist-ZIO/prompt-library) | 主体、媒介、风格转译与实际文字相互配合 | 保留已适合的视觉语言 | 原固定上下双联、品牌、题材与一比一分区不变成通用方法 |
| [Cookbook](https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook) | 核心特征与可变内容分离，列明不应继承的原主体/文字 | 新配方与六维参数 | 实际读cream-curve-editorial、quiet-luxury-furniture-nameplate、prismatic-glass-animal、op-stripe-card、electric-blue-silhouette-product、monochrome-tech-grid各style.json；不打包其图片，不照搬微文案、原比例与固定布局 |
| [IBM插画](https://www.ibm.com/design/language/illustration/overview/)与[技术图](https://www.ibm.com/design/language/infographics/technical-diagrams/design/) | 简洁/表达型素材分工，成套对象语法与准确连接 | PPT说明图与共享素材 | 不继承IBM身份、指定网格数值或对所有节点强加图标 |

维护时先问当前能力缺什么，再借适用做法。常见且适合工作用途的名称已包含瑞士现代、包豪斯、当代编辑、企业现代、极简、双色、孔版、装饰艺术和新艺术等；选择基于表达与识读，不按热度添加整串网络微流派。名称解释与配方之间可以多对多，也可以自主设计。

后续按用途补充的海报/PPT生成项目与具体文件见[来源的设计转译表](sources.md#面向实际用途的外部设计转译)；三模块的常用起点见[推荐](style-recommendations.md)。参考中的主题、品牌和全套模板不随外观参数迁入。
