# -*- coding: utf-8 -*-
import sys
import io

# 设置标准输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json

# 直接复制 _generate_outcomes_table 的逻辑进行测试

product_outcome_map = {
    '1+1+1': {
        '新增境外办学项目': 1,
        '在国外合作学校数': 1,
        '专业合作数量': 2,
        '在校生数': 60,
        '接收国外留学生专业数': 2,
        '接收国外留学生人数': 20,
        '签署校企合作协议及MOA协议数量': 2
    },
    '国际化专业标准': {
        '国际化专业标准数量': 1,
        '资源数量(教材、在线课程)': 2
    },
}

# 测试数据 - 从JSON加载
selected_items = json.loads('[{"name": "1+1+1双学历合作办学", "price": "100000", "unit": "项"}, {"name": "国际化专业标准开发", "price": "50000", "unit": "项"}]')

print('=== 测试映射逻辑 ===')
print('product_outcome_map keys:', list(product_outcome_map.keys()))

# 统计各产品的数量
product_counts = {}
for product in selected_items:
    name = product.get('name', '')
    print(f'Product name: {name}')
    product_counts[name] = product_counts.get(name, 0) + 1

print('\nproduct_counts:', product_counts)

# 检查匹配
print('\n--- 检查匹配 ---')
for product_name, count in product_counts.items():
    print(f'Checking: {product_name}')
    print(f'  In map: {product_name in product_outcome_map}')
    
    # 尝试部分匹配
    for key in product_outcome_map.keys():
        if product_name.startswith(key):
            print(f'  Matches with startswith: {key}')
            break
    else:
        print(f'  No match found')

# 初始化成果指标
outcome_metrics = {
    '新增境外办学项目': 0,
    '在国外合作学校数': 0,
    '专业合作数量': 0,
    '在校生数': 0,
    '国际化专业标准数量': 0,
    '国际化课程标准数量': 0,
    '资源数量(教材、在线课程)': 0,
}

# 根据选择的产品累加成果
print('\n--- 累加成果 ---')
for product_name, count in product_counts.items():
    if product_name in product_outcome_map:
        metrics = product_outcome_map[product_name]
        print(f'Found match: {product_name}')
        for metric, value in metrics.items():
            if metric in outcome_metrics:
                outcome_metrics[metric] += value * count
                print(f'  Added {metric}: +{value * count}')
    else:
        print(f'No match: {product_name}')

print('\nFinal outcome_metrics:', outcome_metrics)