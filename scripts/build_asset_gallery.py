"""维护共享素材的派生预览；默认写入当前技能，--check只读检查一致性。

仅在获得素材库维护授权后生成；普通设计任务使用find_assets只读检索。
不访问网络，不改动源SVG或目录；三个入口共用数据、CSS与界面脚本。
"""
from pathlib import Path
import importlib.util
import json
import re
import argparse
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
outputs={}
spec=importlib.util.spec_from_file_location('assets_index',ROOT/'scripts/find_assets.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
entries=module.load_assets(ROOT)
labels={'icon':'图标','scientific-object':'科学图形','background':'背景','decoration':'装饰','diagram-part':'结构组件','layout-guide':'构图参考'}
rows=[]
for a in entries:
    source=a['source']
    text=' '.join(str(a.get(k,'')) for k in ['id','name','tags','aliases','other_ids','group','family'])+' '+labels[a['kind']]
    rows.append(dict(id=a['id'],slug=a['path'].rsplit('/',1)[-1][:-4],name=a['name'],kind=a['kind'],family=a['family'],group=a.get('group','support'),modules=a['modules'],uses=a['uses'],tone=a.get('tone',''),url=a['path'].removeprefix('assets/'),search=module.normalize(text),note=a.get('note',''),meaning=a.get('meaning',''),source_url=a.get('url') or source.get('url') or '',license=source.get('license','原创资源')))
order={k:i for i,k in enumerate(labels)}
rows.sort(key=lambda a:(order[a['kind']],a['family'],a['id']))
catalogue=json.loads((ROOT/'assets/research/catalogue.json').read_text(encoding='utf-8'))
stats=dict(version=catalogue['version'],checked_on=catalogue['checked_on'],unique_local_files=len(entries),counts=dict(Counter(a['kind'] for a in entries)),families=dict(Counter(a['family'] for a in entries)))
data=dict(stats=stats,assets=rows)
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
outputs['assets/gallery-data.js']='window.VISUAL_ASSET_LIBRARY='+payload+';\n'
outputs['assets/library-stats.json']=json.dumps(stats,ensure_ascii=False,indent=2)+'\n'
template='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__</title><link rel="stylesheet" href="__PREFIX__gallery.css"></head>
<body data-module="__MODULE__" data-prefix="__PREFIX__"><main><h1>__TITLE__</h1><p>__COUNTS__。按实际文件去重；背景明暗版和图标家族变体分别标明。</p><p class="muted">线性和双色图标可以服务不同用途，同一视觉区域优先保持家族一致。科研正文以清晰低干扰为主；箭头与边界属于结构组件，按真实关系编辑。</p>
<div class="presets"><button type="button" data-preset="science">科学图形</button><button type="button" data-preset="paper">科研正文底板</button><button type="button" data-preset="ppt">PPT背景</button><button type="button" data-preset="structure">连线、边界与图例</button></div>
<div class="controls"><div class="row"><input id="query" type="search" aria-label="搜索素材" placeholder="搜索中文或英文，例如：安全、检索、参数、背景"><button id="reset" type="button">清除筛选</button><button id="dark" type="button" aria-pressed="false">深底承载检查</button></div><div class="row" id="kinds" role="group" aria-label="素材类别"></div><div class="row"><label>用途<select id="module"><option value="">全部模块</option><option value="presentation">PPT</option><option value="research">科研</option><option value="poster">海报</option></select></label><label>家族<select id="family"></select></label><label>角色<select id="use"><option value="">全部角色</option><option value="figure-panel">科研正文底板/图形</option><option value="diagram">结构图</option><option value="slide-background">PPT背景</option><option value="slide-content">内容配图</option><option value="teaser">总览主视觉</option><option value="cover">封面</option></select></label><label>背景明暗<select id="tone"><option value="">不限</option><option value="light">浅色</option><option value="dark">深色</option></select></label></div></div>
<p id="status" role="status" aria-live="polite"></p><section id="cards" class="grid" aria-label="素材列表"></section><p id="empty" hidden>当前组合没有匹配项，请减少筛选条件，或按当前内容自主设计。</p><div class="pager"><button id="prev" type="button">上一页</button><span id="page"></span><button id="next" type="button">下一页</button></div>
<footer><p class="note">这些是可复用SVG资源。科学图形中的数量、连接和状态是示意；图表图标不包含实际数据。12类新背景各有明暗版，科研底板另有4个配色，它们不计作新增画风。深底检查中的单色图标反白仅用于检查承载效果。</p><p><a href="__PREFIX__library-stats.json">文件统计</a> · <a href="__PREFIX__design/sources.json">外部来源</a> · 核验于__DATE__</p></footer></main><script src="__PREFIX__gallery-data.js"></script><script src="__PREFIX__gallery-ui.js"></script></body></html>'''
for relative,title,default,prefix in [('assets/gallery.html','共享图标、背景与装饰','',''),('assets/design/gallery.html','海报与PPT素材','presentation','../'),('assets/research/gallery.html','科研素材','research','../')]:
    counts='、'.join(str(stats['counts'][k])+'个'+labels[k] for k in labels)
    text=template.replace('__TITLE__',title).replace('__MODULE__',default).replace('__PREFIX__',prefix).replace('__COUNTS__',counts).replace('__DATE__',stats['checked_on'])
    outputs[relative]=text
if args.check:
    mismatches=[name for name,text in outputs.items() if not (ROOT/name).is_file() or (ROOT/name).read_text(encoding='utf-8')!=text]
    print(json.dumps({'status':'fail' if mismatches else 'pass','mismatches':mismatches},ensure_ascii=False))
    raise SystemExit(1 if mismatches else 0)
for name,text in outputs.items():
    (ROOT/name).write_text(text,encoding='utf-8',newline='\n')
print(json.dumps(stats,ensure_ascii=False))
