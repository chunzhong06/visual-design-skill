"""检查技能的本地引用、配方映射和实际SVG文件，纯标准库且不写文件。

覆盖结构完整性，不判断成图审美、科学语义或外部链接当前可访问性。
可传入另一份技能路径；发现错误返回1，读取失败也写入errors。
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from collections import Counter


def audit(root):
    errors = []
    def local(name, owner):
        path = (root/name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append({'owner':owner, 'missing_or_outside':name})
            return None
        return path
    def read(name):
        return json.loads((root/name).read_text(encoding='utf-8-sig'))
    styles = read('styles/catalogue.json')
    aesthetics = read('aesthetics/catalogue.json')
    style_ids = [s['id'] for s in styles['styles']]
    for kind, ids in [('style',style_ids), ('aesthetic',[s['id'] for s in aesthetics['entries']])]:
        errors.extend({'duplicate_'+kind:key} for key,n in Counter(ids).items() if n>1)
    for item in styles['styles']:
        local('styles/'+item['card'], item['id'])
        if item['family'] not in styles['families']:
            errors.append({'style':item['id'],'unknown_family':item['family']})
        invalid = set(item['roles'])-set(styles['role_names'])
        if invalid: errors.append({'style':item['id'],'unknown_roles':sorted(invalid)})
    for item in aesthetics['entries']:
        local('aesthetics/'+item['card'], item['id'])
        for sid in item['recipe_candidates']:
            if sid not in style_ids: errors.append({'aesthetic':item['id'],'unknown_recipe':sid})
    # 用途推荐必须落到仍存在的配方或科研预设，防止卡片合并后路由悬空。
    recommendations=read('styles/module-recommendations.json')
    profiles=(root/'references/research/visual-profiles.md').read_text(encoding='utf-8')
    if set(recommendations['modules'])!={'poster','presentation','research'}:
        errors.append({'recommendations':'模块集合不完整'})
    for module,group in recommendations['modules'].items():
        rows=group['recommended']+group.get('conditional',[])
        ids=[row['id'] for row in rows]
        if len(ids)!=len(set(ids)):errors.append({'module':module,'recommendations':'重复'})
        for row in rows:
            refs=[row['id']] if row['kind']=='recipe' else row.get('recipes',[])
            for sid in refs:
                if sid not in style_ids:errors.append({'module':module,'unknown_recipe':sid})
            if row['kind']=='research-profile' and row['id'] not in profiles:
                errors.append({'module':module,'unknown_profile':row['id']})
    for path in root.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8-sig')):
            # 离线预览链接可带筛选参数；文件身份由URL的path部分确定。
            link = urlsplit(target.strip('<>'))
            if link.scheme or link.netloc or not link.path: continue
            resolved=(path.parent/unquote(link.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                errors.append({'owner':path.relative_to(root).as_posix(),'bad_link':target})
    counts = {}
    for name in ['assets/research/catalogue.json','assets/design/catalogue.json']:
        catalogue=read(name)
        ids=[a['id'] for a in catalogue['assets']]
        errors.extend({'catalogue':name,'duplicate_asset':key} for key,n in Counter(ids).items() if n>1)
        counts[name]=dict(Counter(a.get('kind','research-object') for a in catalogue['assets']))
        for sid,source in catalogue['sources'].items():
            if source.get('license_file'): local(source['license_file'],sid)
        for item in catalogue['assets']:
            if item['source_id'] not in catalogue['sources']:
                errors.append({'asset':item['id'],'unknown_source':item['source_id']})
            path=local(item['path'],item['id'])
            if path and item.get('sha256') and hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
                errors.append({'asset':item['id'],'hash':'mismatch'})
            # 槽位用相对坐标，只核验容量边界；允许有依据的字图重叠。
            for slot in item.get('slots',[])+item.get('quiet_zones',[]):
                if min(slot['x'],slot['y'],slot['w'],slot['h'])<0 or slot['x']+slot['w']>1.00001 or slot['y']+slot['h']>1.00001:
                    errors.append({'asset':item['id'],'slot':'outside canvas'})
    for path in root.rglob('*.svg'):
        try:
            element=ET.parse(path).getroot()
            box=[float(x) for x in element.get('viewBox','').split()]
            if len(box)!=4 or box[2]<=0 or box[3]<=0: raise ValueError('无有效viewBox')
            if 'background' in path.parts and any(e.tag.endswith('text') for e in element.iter()):
                raise ValueError('无字背景含文字节点')
        except (ET.ParseError,ValueError) as error:
            errors.append({'svg':path.relative_to(root).as_posix(),'error':str(error)})
    return dict(status='pass' if not errors else 'fail',styles=len(style_ids),aesthetics=len(aesthetics['entries']),asset_counts=counts,svg_files=len(list(root.rglob('*.svg'))),errors=errors,scope='本地结构、路径、文件身份和槽位边界；不替代实际成图审阅')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill_path',nargs='?',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    try: result=audit(args.skill_path.resolve())
    except (OSError,ValueError,KeyError,TypeError) as error:
        result={'status':'fail','errors':[str(error)]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='pass' else 1


if __name__=='__main__':
    raise SystemExit(main())
