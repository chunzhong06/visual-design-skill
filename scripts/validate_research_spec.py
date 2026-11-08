"""检查复杂科研图规格的引用和内部一致性，不读图或判断论文事实。

契约见references/research/figure-spec.md。退出0只表示结构检查通过；退出1
表示错误或未解决项；退出2表示输入不可读。只使用标准库且不写文件。
"""
import argparse
import json
from pathlib import Path
import sys


EDGE_KINDS = {'data', 'control', 'dependency', 'message', 'gradient', 'feedback', 'containment', 'causal'}
STAGES = {'training', 'inference', 'shared', 'offline', 'online', 'evaluation'}


def validate(spec):
    """返回结构错误和待核实项；不会把来源字符串当成已核实证据。"""
    errors = []
    unresolved = []
    if not isinstance(spec, dict):
        return {'spec_structure_valid': False, 'errors': ['根节点须为对象'],
                'unresolved': [], 'scientific_truth_verified': False, 'render_inspected': False}
    if spec.get('schema') != 'visual-design/research-figure@1':
        errors.append('schema不匹配')

    def required_text(obj, key, where):
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            errors.append(where + '.' + key + '须为非空文本')

    figure = spec.get('figure')
    if not isinstance(figure, dict):
        errors.append('figure须为对象')
    else:
        for key in ('id', 'kind', 'goal'):
            required_text(figure, key, 'figure')
        width = figure.get('final_width_mm')
        if width is not None and (isinstance(width, bool) or not isinstance(width, (int, float)) or not 0 < width < float('inf')):
            errors.append('final_width_mm须为有限正数')

    def objects(key, required=True):
        value = spec.get(key, [])
        if not isinstance(value, list):
            errors.append(key + '须为数组')
            return []
        if required and not value:
            errors.append(key + '不能为空')
        rows = []
        seen = set()
        for i, item in enumerate(value):
            if not isinstance(item, dict):
                errors.append(key + '[' + str(i) + ']须为对象')
                continue
            identity = item.get('id')
            if not isinstance(identity, str) or not identity.strip():
                errors.append(key + '[' + str(i) + '].id须为非空文本')
                continue
            if identity in seen:
                errors.append(key + '有重复id：' + identity)
            seen.add(identity)
            rows.append(item)
        return rows

    sources = objects('sources')
    source_ids = {item['id'] for item in sources}
    for source in sources:
        required_text(source, 'location', 'source:' + source['id'])
    nodes = objects('nodes')
    edges = objects('edges', required=False)
    groups = {item['id'] for item in objects('groups', required=False)}
    panels = {item['id'] for item in objects('panels', required=False)}
    node_ids = {item['id'] for item in nodes}
    visible = spec.get('visible_text')
    if not isinstance(visible, list) or any(not isinstance(x, str) or not x.strip() for x in visible):
        errors.append('visible_text须为非空字符串的数组')
        visible = []
    visible_set = set(visible)
    symbols = spec.get('symbols', {})
    if not isinstance(symbols, dict) or any(not isinstance(k, str) or not isinstance(v, str) or not k or not v for k, v in symbols.items()):
        errors.append('symbols须为符号到含义的非空文本映射')
        symbols = {}

    def provenance(item):
        refs = item.get('source_refs')
        if not isinstance(refs, list) or not refs or any(not isinstance(x, str) for x in refs):
            errors.append(item['id'] + '缺少有效source_refs')
        elif any(x not in source_ids for x in refs):
            errors.append(item['id'] + '引用未知来源')

    for node in nodes:
        provenance(node)
        required_text(node, 'label', 'node:' + node['id'])
        label = node.get('label')
        if isinstance(label, str) and label not in visible_set:
            errors.append(node['id'] + '标签未列入visible_text')
        for field, choices in (('group', groups), ('panel', panels), ('stage', STAGES)):
            if field in node and (not isinstance(node[field], str) or node[field] not in choices):
                errors.append(node['id'] + '的' + field + '无效')
        repeat = node.get('repeat')
        if repeat is not None and (isinstance(repeat, bool) or not isinstance(repeat, int) or repeat <= 0):
            errors.append(node['id'] + '的repeat须为正整数')
        if 'symbol' in node:
            symbol = node['symbol']
            if not isinstance(symbol, str) or symbol not in symbols:
                errors.append(node['id'] + '使用未定义符号')
            elif 'operator' in node and node['operator'] != symbols[symbol]:
                errors.append(node['id'] + '的符号与算子含义冲突')

    for edge in edges:
        provenance(edge)
        for endpoint in ('from', 'to'):
            if not isinstance(edge.get(endpoint), str) or edge[endpoint] not in node_ids:
                errors.append(edge['id'] + '的' + endpoint + '引用未知节点')
        if not isinstance(edge.get('kind'), str) or edge['kind'] not in EDGE_KINDS:
            errors.append(edge['id'] + '缺少有效连接kind')
        label = edge.get('label', '')
        if not isinstance(label, str):
            errors.append(edge['id'] + '的label须为文本')
        elif label and label not in visible_set:
            errors.append(edge['id'] + '标签未列入visible_text')

    forbidden = spec.get('forbidden_edges', [])
    if not isinstance(forbidden, list):
        errors.append('forbidden_edges须为数组')
        forbidden = []
    for item in forbidden:
        if not isinstance(item, dict):
            errors.append('禁止边须为对象')
            continue
        endpoints_valid = all(isinstance(item.get(k), str) and item[k] in node_ids for k in ('from', 'to'))
        if not endpoints_valid:
            errors.append('禁止边引用未知节点')
            continue
        if 'kind' in item and (not isinstance(item['kind'], str) or item['kind'] not in EDGE_KINDS):
            errors.append('禁止边kind无效')
        for edge in edges:
            if edge.get('from') == item['from'] and edge.get('to') == item['to'] and ('kind' not in item or edge.get('kind') == item['kind']):
                errors.append(edge['id'] + '与禁止边冲突')

    value = spec.get('unresolved', [])
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        errors.append('unresolved须为非空文本项的数组')
    else:
        unresolved = value
    return {'spec_structure_valid': not errors and not unresolved,
            'counts': {'sources': len(sources), 'nodes': len(nodes), 'edges': len(edges)},
            'errors': errors, 'unresolved': unresolved,
            'scientific_truth_verified': False, 'render_inspected': False,
            'note': '检查只覆盖输入结构与引用一致性，科学内容与每张实际成图仍需核验。'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec', type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.spec.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError) as error:
        print('规格读取失败：' + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['spec_structure_valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
