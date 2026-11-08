"""离线查找海报/PPT素材；返回候选，不选画风、不下载或改写文件。

--query按规范化词项求交，中文依赖目录标签而非语义模型。local与
shared-local均有实际文件；共享图标沿原路径引用，不重复复制。
成功返回0，目录、路径或参数错误返回非零退出码。
"""
import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata


def normalize(value):
    text = unicodedata.normalize('NFKC', str(value)).casefold()
    return re.sub(r'[-_\s]+', ' ', text).strip()


def search(entries, query='', kind=None, module=None):
    """按词项及可选类别筛选；词汇排序不代表设计适配得分。"""
    terms = normalize(query).split()
    rows = []
    for entry in entries:
        if kind and entry['kind'] != kind:
            continue
        if module and module not in entry['modules']:
            continue
        haystack = normalize(' '.join(str(entry.get(k, '')) for k in ('id', 'name', 'tags', 'kind')))
        if all(term in haystack for term in terms):
            score = sum(3 if term in normalize(entry['name']) else 1 for term in terms)
            rows.append((score, entry))
    return [entry for _, entry in sorted(rows, key=lambda row: (-row[0], row[1]['id']))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query', default='')
    parser.add_argument('--kind', choices=['layout-guide', 'background', 'decoration', 'icon', 'scientific-object', 'diagram-part'])
    parser.add_argument('--module', choices=['poster', 'presentation'])
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 100:
        parser.error('limit须介于1至100')
    root = Path(__file__).resolve().parents[1]
    try:
        catalogue = json.loads((root/'assets/design/catalogue.json').read_text(encoding='utf-8-sig'))
        matches = search(catalogue['assets'], args.query, args.kind, args.module)
        result = []
        for entry in matches[:args.limit]:
            path = (root/entry['path']).resolve()
            # 共享资产也必须留在本技能内，目录不能把候选引到任意外部文件。
            if not path.is_relative_to(root) or not path.is_file():
                raise ValueError('素材路径失效或越界：'+entry['id'])
            row = dict(entry)
            row['local_path'] = str(path)
            row['source'] = catalogue['sources'][entry['source_id']]
            result.append(row)
        print(json.dumps(dict(query=args.query, total_matches=len(matches), candidates=result,
            network_used=False, note='线框不是成品风格；请按当前材料选择和重排。'), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('素材检索失败：'+str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
