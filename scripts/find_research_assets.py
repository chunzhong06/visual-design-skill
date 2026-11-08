"""离线检索科研素材；只返回候选，不判断科学适配或下载远端文件。

local_path指向已随技能安装的SVG；remote-index仅登记来源路径，采用前仍需
获取并查看实际文件。只使用标准库，不修改项目、技能或网络状态。
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


def search(query, entries, group=None, library=None):
    """按词项求交并排序；别名与标签是词汇索引，不是语义分类器。"""
    terms = normalize(query).split()
    matches = []
    for entry in entries:
        if group and entry.get('group') != group:
            continue
        if library and entry.get('family') != library:
            continue
        haystack = normalize(' '.join(str(entry.get(key, '')) for key in
                             ('id', 'name', 'tags', 'aliases', 'group', 'family')))
        if not all(term in haystack for term in terms):
            continue
        title = normalize(entry.get('name', ''))
        score = sum(5 if term in title else 1 for term in terms)
        if normalize(query) == title:
            score += 20
        matches.append((score, entry))
    return [entry for _, entry in sorted(matches, key=lambda x: (-x[0], x[1]['id']))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--query')
    action.add_argument('--list-sources', action='store_true')
    action.add_argument('--list-groups', action='store_true')
    parser.add_argument('--scope', choices=('local', 'indexed', 'all'), default='local')
    parser.add_argument('--group')
    parser.add_argument('--library', help='例如lucide、opentikz、original、qingicon')
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    if args.query is not None and not args.query.strip():
        parser.error('检索词不能为空')
    if not 1 <= args.limit <= 100:
        parser.error('limit须在1至100之间')
    root = Path(__file__).resolve().parents[1]
    try:
        catalogue = json.loads((root / 'assets/research/catalogue.json').read_text(encoding='utf-8-sig'))
        if args.list_sources:
            result = {'sources': catalogue['sources'], 'network_used': False}
        elif args.list_groups:
            result = {'groups': catalogue['groups']}
        else:
            if args.group and args.group not in catalogue['groups']:
                parser.error('未知group；可用--list-groups查看')
            entries = []
            if args.scope in ('local', 'all'):
                entries.extend(catalogue['assets'])
            if args.scope in ('indexed', 'all'):
                index = json.loads((root / 'assets/research/external-index.json').read_text(encoding='utf-8-sig'))
                entries.extend(index['entries'])
            matches = search(args.query, entries, args.group, args.library)
            rows = []
            for entry in matches[:args.limit]:
                row = dict(entry)
                if entry.get('path'):
                    path = (root / entry['path']).resolve()
                    if not path.is_relative_to(root) or not path.is_file():
                        raise ValueError('本地素材路径失效或越界：' + entry['id'])
                    row['local_path'] = str(path)
                source = catalogue['sources'][entry['source_id']]
                row['source_checked_on'] = source['checked_on']
                row['license'] = source.get('license') if entry.get('license') is None else entry['license']
                rows.append(row)
            result = {'query': args.query, 'scope': args.scope, 'total_matches': len(matches),
                      'returned': len(rows), 'candidates': rows, 'network_used': False,
                      'note': '结果是素材候选；remote-index并非本地文件，科学含义与实际外观须结合当前任务核对。'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('素材检索失败：' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
