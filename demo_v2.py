"""
演示脚本 v2.0 - 展示新增功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import SolutionGenerator
from parsers.excel_parser import ExcelParser


def demo_new_features():
    """演示新功能"""
    print("\n" + "="*60)
    print("职业教育国际化方案生成器 v2.0 - 新功能演示")
    print("="*60)

    # 演示1: 中资企业字段
    print("\n【演示1】中资企业字段")
    print("-" * 60)

    config = {
        "school_name": "广西现代职业技术学院",
        "partner_country": "印度",
        "partner_institution": "菲律宾南洋理工大学",
        "chinese_enterprise": "青山控股集团",  # 新增字段
        "major": "工业机器人",
        "project_name": "中国-东盟工业机器人工匠学院",
    }

    generator = SolutionGenerator(config)
    print(f"学校: {config['school_name']}")
    print(f"合作国家: {config['partner_country']}")
    print(f"合作院校: {config['partner_institution']}")
    print(f"中资企业: {config['chinese_enterprise']} [OK]")
    print(f"专业: {config['major']}")

    output_file = generator.generate("output/演示_含中资企业.docx")
    print(f"\n生成的文件: {output_file}")

    # 演示2: Excel产品选择
    print("\n【演示2】从Excel加载产品列表")
    print("-" * 60)

    parser = ExcelParser("厚溥国际职业教育国际化产品报价单2026版(2.0).xlsx")
    products = parser.get_all_products_for_selection()

    print(f"共加载 {len(products)} 个可选产品:")
    for i, product in enumerate(products[:5], 1):  # 显示前5个
        print(f"  {i}. {product['name']} - {product['price']}{product['unit']}")

    if len(products) > 5:
        print(f"  ... 还有 {len(products) - 5} 个产品")

    # 演示3: 带选择产品的方案生成
    print("\n【演示3】基于选择的产品生成方案")
    print("-" * 60)

    # 模拟选择了3个产品
    selected = [
        products[0] if products else {"name": "海外院校对接服务", "price": "5", "unit": "项"},
        products[5] if len(products) > 5 else {"name": "校级专业标准认证", "price": "5", "unit": "个"},
        products[10] if len(products) > 10 else {"name": "校级课程标准认证", "price": "4", "unit": "门"},
    ]

    config_with_selection = config.copy()
    config_with_selection['selected_items'] = selected
    config_with_selection['custom_items'] = []
    config_with_selection['excel_products'] = products

    generator2 = SolutionGenerator(config_with_selection)
    output_file2 = generator2.generate("output/演示_含产品选择.docx")

    print(f"选择了 {len(selected)} 个产品:")
    for item in selected:
        print(f"  - {item.get('name', '')}: {item.get('price', '')}{item.get('unit', '')}")
    print(f"\n生成的文件: {output_file2}")

    # 演示4: 自定义项目
    print("\n【演示4】添加自定义建设内容")
    print("-" * 60)

    custom_items = [
        {
            "name": "校企合作实训基地建设",
            "description": "与青山控股集团在印尼共建实训基地，提供学生实习岗位。",
            "price": 150000
        },
        {
            "name": "数字化教学平台开发",
            "description": "开发支持中文和印尼语的双语在线学习平台。",
            "price": 80000
        }
    ]

    config_with_custom = config.copy()
    config_with_custom['selected_items'] = selected
    config_with_custom['custom_items'] = custom_items
    config_with_custom['excel_products'] = products

    generator3 = SolutionGenerator(config_with_custom)
    output_file3 = generator3.generate("output/演示_含自定义项目.docx")

    print(f"添加了 {len(custom_items)} 个自定义项目:")
    for item in custom_items:
        print(f"  - {item['name']}: {item['price']}元")
    print(f"\n生成的文件: {output_file3}")

    # 总结
    print("\n" + "="*60)
    print("所有演示完成!")
    print("="*60)
    print("\n新增功能总结:")
    print("  [OK] 中资企业字段 - 在配置和方案中体现合作企业")
    print("  [OK] 产品动态选择 - 从Excel加载并勾选需要的产品")
    print("  [OK] 自定义项目 - 添加不在Excel中的特殊需求")
    print("  [OK] 智能预算生成 - 基于选择和自定义内容自动生成预算")
    print("\n生成的文件位于 output/ 目录")
    print("可以用 Microsoft Word 或 WPS 打开查看和编辑\n")


if __name__ == "__main__":
    demo_new_features()
