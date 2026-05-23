import json
from generators.content_builder import ContentBuilder

# 模拟从表单解析的数据
config = {
    'school_name': '测试学校',
    'partner_country': '印尼',
    'partner_institution': '印尼大学',
    'chinese_enterprise': '青山集团',
    'major': '工业机器人',
    'project_name': '中国-印尼工业机器人工匠学院',
    'selected_items': [
        {'name': '1+1+1双学历合作办学', 'price': '100000', 'unit': '项'},
        {'name': '国际化专业标准开发', 'price': '50000', 'unit': '项'}
    ],
    'custom_items': []
}

builder = ContentBuilder(config)

print('=== Testing ContentBuilder ===')
print('selected_items:', config['selected_items'])
print('selected_items length:', len(config['selected_items']))

# 测试各章节构建
print('\n--- Section 3 ---')
s3 = builder._build_section3_content()
print('Section 3:', s3)

print('\n--- Section 5 ---')
s5 = builder._build_section5_outcomes()
print('Section 5:', s5)

print('\n--- All Sections ---')
all_sections = builder.build_all_sections()
for key, value in all_sections.items():
    print(f'{key}: {value}')