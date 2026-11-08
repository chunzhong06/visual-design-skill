# 外部项目的借鉴方法

用于理解参考图、扩展方法或维护技能时按需阅读。下面是从原始资料提炼并独立改写的做法，既不要求运行外部项目，也不替换现有生图插件。链接核验于2026-11-08。

| 来源 | 借鉴什么 | 在本技能怎样使用 |
|---|---|---|
| [AI Visual Prompt Cookbook](https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook/blob/main/CONTRIBUTING.md) | 内容变量与可保留的视觉特征分开，说明参考内容中不该继承的部分 | 保留六维风格特征，替换主体、文案和场景；参考图中的人物、品牌与原文不自动迁入新任务 |
| [AI Image Prompts](https://github.com/horushe93/ai-image-prompts) | 参数化模板、具体案例与不同画幅预览分开 | 同一视觉语言可服务不同用途；横竖转换由模块重新组织，不仅裁切 |
| [Amazing Posters](https://github.com/posterlet/amazing-posters) | 将格式、颜色、布局、主体和准确文案分别说明 | 组装提示词时保留各自职责，避免只有“高级、震撼”等形容词；固定示例布局不写成画风规则 |
| [2slides PPT Prompts](https://github.com/2slides/awesome-nano-banana-ppt-prompts) | 用预览、用途标签与提示词组织实例 | 图与说明紧邻，按图片角色查找做法；漂亮案例不自动等于适用于当前内容 |
| [Slidev布局](https://sli.dev/builtin/layouts)与[主题](https://sli.dev/guide/write-theme) | 覆盖封面、章节、左右图文、双栏与结论等角色，并把整体外观与功能分开 | PPT模块按本页表达目的选布局；共同视觉参数交给风格路由，不把布局名登记为画风 |
| [Marpit图片](https://marpit.marp.app/image-syntax) | 区分背景、行内素材和分区图片，明确填满与完整显示的取舍 | 主视觉可定向裁切，流程和关键标签优先完整显示；留白对应实际文本区 |
| [Presenton模板](https://docs.presenton.ai/user-guide/branding-and-design/templates)与[媒体](https://docs.presenton.ai/user-guide/working-with-content/images-and-media) | 布局和可编辑区域与全局颜色、字体分开；图片可局部替换和调整焦点 | 先定图片分工和文字承载方式，再生成；改图时维持已有布局和关键对象 |
| [IBM插画](https://www.ibm.com/design/language/illustration/overview/)与[图形符号](https://www.ibm.com/design/language/iconography/pictograms/design/) | 成套语法保持一致，表达型与简洁型图形按场景使用 | 封面允许强表现，解释图控制细节；统一形状、线条与颜色语义，不复制品牌身份 |
| [Lucide](https://lucide.dev/contribute/icons/design-principles)与[OpenMoji](https://www.openmoji.org/styleguide/) | 整套符号统一线宽、端点、圆角、比例与细节层次 | 同组图标不随意混用不同家族；各库的24或32像素网格属于原库制作规范，不直接套作PPT尺寸 |
| [MidJourney参考库](https://github.com/willwulfken/MidJourney-Styles-and-Keywords-Reference) | 分类观察媒介与视觉特征，结合对照理解效果 | 用具体特征描述画风；特定模型版本、权重和语法不当作现有生图插件参数 |

借鉴一项做法时明确归属：阅读顺序、版式和关系进入方法模块；色彩、线条、造型、光影、材质和字形进入风格说明；文件、来源、透明度和复用方式进入素材处理。对参考案例的具体题材、文字、数字、模型接口和签名分别核对，不随结构一同复制。

针对海报和PPT补强时，进一步按[案例转译](case-patterns.md)读取原设计方、演示方法与实际仓库文件。具体构图见[海报方法](poster-composition.md)，页面家族与证据见[PPT方法](presentation-composition.md)，可用文件见[设计素材](design-materials.md)。

## 产品传播与工作演示

参考公开项目的实际说明后，先决定内容如何被看见，再选媒介。Skiff、MIND与Atera的设计方说明都把定位、语气与成套字形/图形联系起来，不能只提取表面效果。PPT-Design-Prompt强调单图的逐页主旨、角色和文字安全区；这些应转为方法条件，而不是全页照抄其固定数值或偏好。

真实产品可用原截图作为传播主体，与生成的主视觉或背景共同排版。机制图按说明需要使用；背景、对象配图、准确流程和证据截图承担不同作用。来源及实际阅读范围见[说明](sources.md)。
