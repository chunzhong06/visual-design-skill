"""离线定位美学别名；只返回提及和上下文，不判断否定、引用或最终路由。

仅使用Python标准库，不读写项目内容或访问网络。span为规范化文本中的
半开区间，不能直接用于修改原请求。JSON/路径错误经CLI返回非零退出码。
"""
from pathlib import Path
import argparse
import json
import re
import sys
import unicodedata


def normalize(text):
    text = unicodedata.normalize('NFKC', text).casefold()
    text = re.sub(r'[-‐‑‒–—_]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def alias_pattern(alias):
    # 英文词边界只约束字母数字，允许中文与英文名称直接相邻。
    left = r'(?<![a-z0-9])' if re.match(r'[a-z0-9]', alias[0]) else ''
    right = r'(?![a-z0-9])' if re.match(r'[a-z0-9]', alias[-1]) else ''
    return re.compile(left + re.escape(alias) + right)


def resolve(query, catalogue):
    """返回最长非重叠名称；同一位置的同义歧义候选全部保留。

    不合并多次提及，因为同一名称可能先被排除、后被局部借鉴。
    完整语义和作用范围需由调用者结合query_original解释。
    """
    text = normalize(query)
    candidates = []
    for entry in catalogue['entries']:
        for alias in dict.fromkeys(normalize(x) for x in entry['aliases']):
            for match in alias_pattern(alias).finditer(text):
                candidates.append((match.start(), match.end(), alias, entry))
    groups = {}
    for start, end, alias, entry in sorted(candidates, key=lambda x: (-(x[1]-x[0]), x[0])):
        span = (start, end)
        if span not in groups and any(start < b and a < end for a, b in groups):
            continue
        groups.setdefault(span, {})[entry['id']] = (alias, entry)
    matches = []
    for (start, end), entries in sorted(groups.items()):
        matches.append(dict(span=[start, end], mention=text[start:end],
            context=text[max(0, start-32):min(len(text), end+32)],
            candidates=[dict(id=e['id'], name=e['name'], card='aesthetics/' + e['card'])
                        for alias, e in entries.values()],
            ambiguous=len(entries) > 1))
    context_terms = []
    for term in catalogue.get('context_terms', []):
        occurrences = []
        for alias in dict.fromkeys(normalize(x) for x in term['aliases']):
            for match in alias_pattern(alias).finditer(text):
                a, b = match.span()
                # 具体名称内的宽泛词不另生成提示，避免同一处反复转译。
                if not any(start <= a and b <= end for start, end in groups):
                    occurrences.append([a, b])
        if occurrences:
            context_terms.append(dict(term=term['term'], spans=sorted({tuple(x) for x in occurrences}),
                interpretations=term['interpretations'], action=term['action']))
    return dict(query_original=query, normalized_query=text,
        matches=matches, context_terms=context_terms,
        interpretation_required=True,
        note='仅定位提及；请结合完整请求判断肯定、排除、比较和局部参考，再用共享路由形成设计。未命中不代表没有可用风格。')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--query', help='原始请求；不含自动选择含义')
    group.add_argument('--query-file', type=Path, help='UTF-8原始请求文件')
    args = parser.parse_args()
    try:
        query = args.query if args.query is not None else args.query_file.read_text(encoding='utf-8-sig')
        if not query.strip():
            parser.error('请求文本不能为空')
        path = Path(__file__).resolve().parents[1] / 'aesthetics/catalogue.json'
        catalogue = json.loads(path.read_text(encoding='utf-8-sig'))
        print(json.dumps(resolve(query, catalogue), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError) as error:
        print(f'名称定位失败：{error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
