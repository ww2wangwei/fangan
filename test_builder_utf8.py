# -*- coding: utf-8 -*-
import json
from generators.content_builder import ContentBuilder

# 模拟从表单解析的数据 - 使用中文字符
config = {
    'school_name': '武汉职业技术学院',
    'partner_country': '印度尼西亚',
    'partner_institution': '泗水理工大学',
    'chinese_enterprise': '青山控股集团',
    'major': '工业机器人技术',
    'project_name': '中国-印度尼西亚工业机器人技术工匠学院',
    'selected_items': [
        {'name': '1+1+1双学历合作办学', 'price': '100000', 'unit': '项'},
        {'name': '国际化专业标准开发', 'price': '50000', 'unit': '项'}
    ],
    'custom_items': []
}

builder = ContentBuilder(config)

print('=== Testing ContentBuilder ===')
print('selected_items:', builder.selected_items)
print('selected_items length:', len(builder.selected_items))

# 检查产品名称
print('\n--- Product Names ---')
for p in builder.selected_items:
    name = p.get('name', '')
    print(f'  Name: {name} | Type: {type(name)}')

# 测试第5章
print('\n--- Section 5 ---')
s5 = builder._build_section5_outcomes()
print('Section 5 result:', s5)

# 测试产品匹配
print('\n--- Testing Product Matching ---')
product_outcome_map = {
    '1+1+1': {'新增境外办学项目': 1},
    '国际化专业标准': {'国际化专业标准数量': 1}
}

for p in builder.selected_items:
    name = p.get('name', '')
    in_map = name in product_outcome_map
    print(f'  {name} in map: {in_map}')