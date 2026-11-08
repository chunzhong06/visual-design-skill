# 复杂科研图的内部规格

用于复杂拓扑、多面板、严格编辑或反复修改的图。简单图用等效短清单，不要求用户写JSON。规格固定科学内容，视觉方案可以调整被允许的维度；规格校验不查看图片，也不证明来源断言真实。

## 最小结构

JSON对象使用schema值`visual-design/research-figure@1`：

- figure：id、kind、goal；可加purpose、language、final_width_mm。
- sources：对象数组，每项有唯一id与location（文档/URL/文件及章节、页码或实现位置）。
- nodes：每项有唯一id、准确label、非空source_refs；可加group、panel、stage、operator、symbol、repeat等。
- edges：每项有唯一id、from、to、kind、非空source_refs；可加label、line、condition。kind使用data/control/dependency/message/gradient/feedback/containment/causal。
- visible_text：允许出现在图中的准确字符串数组，覆盖所有节点label及非空边label；制作指令和图注不列入时不得入图。
- 可选groups与panels：每项有唯一id、label。节点若声明group/panel，引用必须存在。
- 可选symbols：符号到含义的字典；节点同时声明operator和symbol时含义一致。
- 可选forbidden_edges：from、to及可选kind，表示来源要求禁止的捷径；不能与已声明连接冲突。
- 可选unresolved：未确定的科学事实。非空时记录结构待核实，先解决影响最终含义的项目。

节点stage按需使用training/inference/shared/offline/online/evaluation。repeat只有可靠的正整数；未知时省略，不以占位数字通过检查。可见文字清单只放实际上需要的字符串。

## 校验

运行`python scripts/validate_research_spec.py 项目中的spec.json`。脚本核对字段、ID、来源引用、端点、可见标签、阶段、重复、符号和禁止边，返回JSON。退出0表示规格结构检查通过；退出1表示结构错误或仍有未解决项；退出2表示文件或JSON不可读。

复杂图将该规格用于[生成与逐项目检](generation-and-review.md)。脚本不证明引文真实、方法正确、图像中对象存在或箭头画对。每张新图仍需实际查看，对照全部节点和边，再扫描多出的连接；图形改变后重新检查。
