"""统一检查结构、素材、派生预览与公开包边界；只读，不连接网络。

--public用于准备分发的目录，拒绝个人local文件；日常安装检查可省略。
它不评价成图审美、科学语义或外部网址，不取代实际看图。
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from validate_design_library import audit


def validate(root, public=False):
    root=root.resolve()
    report=audit(root)
    errors=list(report['errors'])
    required=['README.md','LICENSE','THIRD_PARTY_NOTICES.md','LICENSES/PROJECT-MIT.txt','.gitignore']
    for name in required:
        if not (root/name).is_file():errors.append({'release':'missing','path':name})
    frontmatter=(root/'SKILL.md').read_text(encoding='utf-8')
    if not re.search(r'^name:\s*visual-design\s*$',frontmatter,re.M):errors.append({'release':'invalid skill name'})
    if public and (root/'local').exists() and any(p.is_file() for p in (root/'local').rglob('*')):
        errors.append({'release':'private local files present'})
    if (root/'.gitignore').is_file() and '/local/' not in (root/'.gitignore').read_text(encoding='utf-8').splitlines():
        errors.append({'release':'local directory is not ignored'})
    # 只报告命中路径和种类，不回显可能敏感的实际内容。
    patterns={
        'private-windows-path':re.compile(r'[A-Za-z]:[\\/]+Users[\\/]+',re.I),
        'private-chat-cache':re.compile(r'wxid_[a-z0-9_]+|Wechat\sFiles',re.I),
        'private-key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
        'credential':re.compile(r'(?<![\w])(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-[A-Za-z0-9]{30,})'),
    }
    for path in root.rglob('*'):
        if not path.is_file() or any(part in ['.git','local','__pycache__'] for part in path.relative_to(root).parts):continue
        try:text=path.read_text(encoding='utf-8-sig')
        except UnicodeError:continue
        for kind,pattern in patterns.items():
            if pattern.search(text):errors.append({'release':kind,'path':path.relative_to(root).as_posix()})
    # 实际纳入的第三方资源必须有可随包保存的许可，远端索引不在此计数。
    sources={}
    for category in ['research','design']:
        catalogue=json.loads((root/f'assets/{category}/catalogue.json').read_text(encoding='utf-8'))
        for asset in catalogue['assets']:
            source=catalogue['sources'][asset['source_id']]
            sources[asset['path']]=asset['source_id']
            if not source.get('license_file'):
                errors.append({'release':'missing local asset license','path':asset['path'],'source':asset['source_id']})
    result=subprocess.run([sys.executable,'-B',str(root/'scripts/build_asset_gallery.py'),'--check'],capture_output=True,text=True)
    if result.returncode:errors.append({'release':'derived gallery differs'})
    report.update(status='fail' if errors else 'pass',errors=errors,public_distribution=public,local_asset_files=len(sources),gallery='pass' if result.returncode==0 else 'fail',scope='结构、文件身份、派生预览、许可位置和公开边界；不替代成图审阅')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--public',action='store_true')
    parser.add_argument('skill_path',nargs='?',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    try:result=validate(args.skill_path,args.public)
    except (OSError,ValueError,KeyError,TypeError) as error:result={'status':'fail','errors':[str(error)]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='pass' else 1


if __name__=='__main__':raise SystemExit(main())
