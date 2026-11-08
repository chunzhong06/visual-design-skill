"""按用途检索实际本地素材，合并科研与设计目录并按文件路径去重。

旧的分模块检索入口继续可用。本入口不访问网络、不选择画风、不修改文件；
词项求交依赖中英标签，不是语义适配评分。--use可把科研正文底板与
封面背景分开，具体用法仍须结合材料核对。成功返回0，错误返回2。
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata

KINDS=['icon','scientific-object','background','decoration','diagram-part','layout-guide']


def normalize(value):
    text=unicodedata.normalize('NFKC',str(value)).casefold()
    return re.sub(r'[-_\s]+',' ',text).strip()


def load_assets(root):
    """同一路径合并模块与别名；副本身份冲突时报错，避免重复计数。"""
    merged={}
    for name in ['research','design']:
        catalogue=json.loads((root/'assets'/name/'catalogue.json').read_text(encoding='utf-8-sig'))
        for original in catalogue['assets']:
            entry=dict(original)
            path=(root/entry['path']).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                raise ValueError('素材路径失效或越界：'+entry['id'])
            key=path.relative_to(root).as_posix()
            entry.setdefault('kind','icon' if entry['source_id']=='lucide' else 'scientific-object')
            entry.setdefault('modules',['research'] if name=='research' else ['poster','presentation'])
            entry.setdefault('family','original')
            entry.setdefault('uses',['diagram','cover','teaser','slide-content','figure-panel'] if entry['kind'] in ('icon','scientific-object') else [])
            entry['source']=catalogue['sources'][entry['source_id']]
            if key not in merged:
                entry['other_ids']=[];entry['catalogues']=[name]
                merged[key]=entry
                continue
            old=merged[key]
            if old.get('sha256')!=entry.get('sha256'):
                raise ValueError('共享文件身份冲突：'+key)
            old['modules']=sorted(set(old['modules']+entry['modules']))
            old['uses']=sorted(set(old['uses']+entry['uses']))
            old['aliases']=list(dict.fromkeys(old.get('aliases',[])+entry.get('aliases',[])+[entry['name']]))
            old['other_ids']=list(dict.fromkeys(old['other_ids']+[entry['id']]))
            old['catalogues'].append(name)
    return list(merged.values())


def search(entries,query='',module=None,kinds=None,family=None,group=None,use=None,tone=None):
    terms=normalize(query).split()
    found=[]
    for item in entries:
        if module and module not in item['modules']:continue
        if kinds and item['kind'] not in kinds:continue
        if family and item['family']!=family:continue
        if group and item.get('group')!=group:continue
        if use and use not in item['uses']:continue
        if tone and item.get('tone')!=tone:continue
        text=normalize(' '.join(str(item.get(k,'')) for k in ['id','name','tags','aliases','other_ids','group','family']))
        if not all(t in text for t in terms):continue
        score=sum(4 if t in normalize(item['name']) else 1 for t in terms)
        found.append((score,item))
    return [x for _,x in sorted(found,key=lambda pair:(-pair[0],pair[1]['id']))]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query',default='')
    parser.add_argument('--module',choices=['poster','presentation','research'])
    parser.add_argument('--kind',action='append',choices=KINDS)
    parser.add_argument('--family')
    parser.add_argument('--group')
    parser.add_argument('--use',help='例如figure-panel、diagram、slide-background、teaser')
    parser.add_argument('--tone',choices=['light','dark'])
    parser.add_argument('--limit',type=int,default=12)
    parser.add_argument('--list',choices=['kinds','groups','families','uses','stats'])
    args=parser.parse_args()
    if not 1<=args.limit<=200:parser.error('limit须在1至200之间')
    root=Path(__file__).resolve().parents[1]
    try:
        entries=load_assets(root)
        matches=search(entries,args.query,args.module,args.kind,args.family,args.group,args.use,args.tone)
        if args.list:
            fields={'kinds':'kind','groups':'group','families':'family','uses':'uses'}
            if args.list=='stats':result={'unique_local_files':len(matches),'counts':dict(Counter(x['kind'] for x in matches))}
            else:
                field=fields[args.list]
                values=[v for x in matches for v in (x[field] if field=='uses' else [x.get(field,'other')])]
                result=dict(sorted(Counter(values).items()))
        else:
            rows=[]
            for item in matches[:args.limit]:
                row=dict(item);row['local_path']=str((root/item['path']).resolve());rows.append(row)
            result=dict(query=args.query,scope='local',unique_matches=len(matches),returned=len(rows),candidates=rows,
                network_used=False,note='按实际文件去重；素材语义、表现强度与真实连接仍由当前内容确定。')
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError) as error:
        print('共享素材检索失败：'+str(error),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
