# -*- coding: utf-8 -*-
import sys
import io

# 设置标准输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 模拟 Flask 接收表单数据后的处理
import json
from generators.content_builder import ContentBuilder

# 模拟从浏览器传来的数据
test_form_data = {
    'school_name': '武汉职业技术学院',
    'partner_country': '印度尼西亚',
    'partner_institution': '泗水理工大学',
    'chinese_enterprise': '青山控股集团',
    'major': '工业机器人技术',
    'project_name': '中国-印度尼西亚工业机器人技术工匠学院',
    'selected_items': json.dumps([
        {'name': '1+1+1双学历合作办学', 'price': '100000', 'unit': '项'},
        {'name': '国际化专业标准开发', 'price': '50000', 'unit': '项'}
    ], ensure_ascii=False),
    'custom_items': json.dumps([], ensure_ascii=False),
}

# 模拟 app.py 的处理逻辑
config = {
    'school_name': test_form_data.get('school_name', ''),
    'partner_country': test_form_data.get('partner_country', ''),
    'partner_institution': test_form_data.get('partner_institution', ''),
    'chinese_enterprise': test_form_data.get('chinese_enterprise', ''),
    'major': test_form_data.get('major', ''),
    'project_name': test_form_data.get('project_name', '')
}

# 解析选择的产品
try:
    config['selected_items'] = json.loads(test_form_data['selected_items'])
    config['custom_items'] = json.loads(test_form_data['custom_items'])
except json.JSONDecodeError as e:
    print(f'JSON解析错误: {e}')
    config['selected_items'] = []
    config['custom_items'] = []

print('=== 配置加载完成 ===')
print(f'selected_items: {config["selected_items"]}')

# 创建 ContentBuilder
builder = ContentBuilder(config)

print('\n=== ContentBuilder 初始化 ===')
print(f'school_name: {builder.school_name}')
print(f'selected_items count: {len(builder.selected_items)}')

# 显示产品名称
print('\n--- 产品名称 ---')
for i, p in enumerate(builder.selected_items):
    name = p.get('name', '')
    print(f'{i+1}. Name: {name}')

# 测试第5章生成
print('\n--- 第5章生成测试 ---')
s5 = builder._build_section5_outcomes()
print(f'Section 5 result: {s5}')

# 测试 _generate_outcomes_table 方法
print('\n--- 直接测试 _generate_outcomes_table ---')
table = builder._generate_outcomes_table()
print(f'Table result: {table}')
print(f'Table length: {len(table)}')