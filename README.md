# visual-design · 工作视觉设计

为现有生图能力补上内容组织、风格选择和结果核验，服务**海报、PPT与计算机/AI科研配图**。

这是一个辅助技能，不内置付费生图后端。它从材料确定图片要说明什么，再选择适合的视觉语言；已有风格都不合适时允许自主设计。模块负责方法，风格负责外观，素材负责实现。

## 能做什么

| 用途 | 方法能力 | 常用视觉起点 |
|---|---|---|
| 海报 | 主张、主题对象、字图层级、观看顺序与跨画幅 | 半调印刷、木刻套色、编辑摄影、几何色面、重字形、衬线编辑 |
| PPT配图 | 封面、背景、概念、流程、对比、场景和独立素材的分工 | 中性编辑、平面插画、精密线描、哑光立体、几何色面、半调印刷 |
| 科研 | 图组分工、方法架构、局部机制、实验流程、多面板及科学关系核对 | 中性精密矢量、柔彩语义分区、高反差几何技术；插画与空间表达按需采用 |

一个入口、三个方法模块、一层共享风格路由。25张六维视觉参数卡、20个工作设计名称解释，534个本地SVG以及1247条远端索引。计数分别描述配方、解释和资源，不相加当作画风数量。

## 安装

在支持skill的Codex中，可让安装器从本仓库安装，并指定技能名 `visual-design`：

```text
使用 skill-installer 从 https://github.com/chunzhong06/visual-design-skill 安装根目录的技能，名称 visual-design，安装为用户级通用技能。
```

也可将整个仓库放到当前客户端支持的用户级skill目录，目录命名为 `visual-design`，使 `SKILL.md` 位于该目录根部。当前官方文档列出的用户级位置为 `~/.agents/skills/`，项目级为 `.agents/skills/`；旧版客户端或安装器可能使用其他兼容位置，按当前客户端选择一个位置，避免同名重复安装。见[OpenAI官方技能文档](https://learn.chatgpt.com/docs/build-skills)。

辅助脚本需要Python 3.10或更新版本，仅用标准库。正常使用需要宿主提供可用的生图能力；完整PPT文件由宿主的演示文稿流程完成，本技能负责其中的图片设计。真实曲线、统计图和数值热图由真实数据绘图流程制作。

## 自然语言调用

```text
给我生成一张这个项目的海报，材料如下……
给我生成PPT，使用生图插件生成背景、概念图和流程配图……
根据这篇论文的方法与实现生成架构图，重点说明……
```

也可显式调用 `$visual-design`。无需知道美学名称；可以用“线条更清楚”“像印刷”“背景安静一些”等方式反馈。整体方向未定时先给三个标注清楚的方向，已有方案则直接沿用。

## 素材与风格入口

- [风格配方](styles/index.md)与[模块推荐](references/style-recommendations.md)
- [名称解释](aesthetics/index.md)、[共享路由](references/style-router.md)
- 下载后在浏览器打开 `assets/gallery.html`，按用途、类别、家族和角色筛选实际SVG
- [专业图形选择](references/material-selection.md)与[科研视觉词汇](references/research/visual-vocabulary.md)

```sh
python scripts/find_assets.py --module research --kind scientific-object --query "特征 选择"
python scripts/find_assets.py --module presentation --kind background --tone light
python scripts/find_assets.py --list stats
```

识别符号与局部操作图解共同帮助理解。素材中的格数、节点、维度和曲线不自动成为当前研究事实；生成后核对全部必要关系。目录只是词项检索，返回顺序不是审美或科学适配评分。

## 个人偏好

公开版本默认中性。需要个性化时参照[偏好示例](references/preferences.example.md)，在安装目录建立 `local/preferences.md`；该目录不提交Git，也不进入公开分发包。当前请求、项目方案和准确内容优先，风格喜好不覆盖科学结构与可读性。

## 维护与检查

```sh
python scripts/validate_release.py --public
```

该入口检查内部链接、配方和推荐映射、素材身份、派生预览与公开包边界。日常安装允许本地偏好时省略 `--public`。检查覆盖可确定的结构和资源，实际成图仍需看图核对语义、文字、连接和最终尺寸。

更新素材目录后运行 `python scripts/build_asset_gallery.py`，再执行检查。[贡献说明](CONTRIBUTING.md)记录风格、素材与方法的收录边界。

## 许可与致谢

原创说明、风格参数和原创SVG使用[CC BY 4.0](LICENSE)；原创辅助代码使用[MIT](LICENSES/PROJECT-MIT.txt)；第三方图形保留各自许可。起点来自[Nihilist-ZIO/prompt-library](https://github.com/Nihilist-ZIO/prompt-library)，结合其他设计项目与真实论文图独立整理。完整归属、改编范围和具体来源见[第三方声明](THIRD_PARTY_NOTICES.md)与[来源说明](references/sources.md)。
