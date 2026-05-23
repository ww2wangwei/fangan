"""
演示脚本 - 展示方案生成器的完整功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import SolutionGenerator
from parsers.excel_parser import ExcelParser


def demo1_basic():
    """演示1: 基本用法"""
    print("\n" + "="*60)
    print("演示1: 基本用法 - 生成标准方案")
    print("="*60)

    config = {
        "school_name": "广西现代职业技术学院",
        "partner_country": "印度",
        "partner_institution": "菲律宾南洋理工大学",
        "major": "工业机器人",
        "project_name": "中国-东盟工业机器人工匠学院",
    }

    generator = SolutionGenerator(config)
    generator.print_config()

    output_file = generator.generate("output/演示1_标准方案.docx")
    print(f"\n生成的文件: {output_file}")


def demo2_custom():
    """演示2: 自定义配置"""
    print("\n" + "="*60)
    print("演示2: 自定义配置 - 不同国家和专业")
    print("="*60)

    config = {
        "school_name": "深圳职业技术学院",
        "partner_country": "泰国",
        "partner_institution": "曼谷皇家理工大学",
        "major": "新能源汽车技术",
        "project_name": "中泰新能源汽车工匠学院",
    }

    generator = SolutionGenerator(config)
    output_file = generator.generate("output/演示2_定制方案.docx")
    print(f"\n生成的文件: {output_file}")


def demo3_pricing():
    """演示3: 加载报价单"""
    print("\n" + "="*60)
    print("演示3: 加载报价单数据")
    print("="*60)

    # 解析Excel报价单
    excel_file = "厚溥国际职业教育国际化产品报价单2026版(2.0).xlsx"

    if os.path.exists(excel_file):
        parser = ExcelParser(excel_file)
        data = parser.parse_all()

        print(f"\n解析结果:")
        for sheet_name, items in data.items():
            print(f"  {sheet_name}: {len(items)} 条记录")

        # 导出为JSON缓存
        cache_file = parser.export_to_json("data/cache.json")
        print(f"\n缓存文件: {cache_file}")
    else:
        print(f"\n报价单文件不存在: {excel_file}")


def demo4_batch():
    """演示4: 批量生成"""
    print("\n" + "="*60)
    print("演示4: 批量生成 - 多个专业方案")
    print("="*60)

    base_config = {
        "school_name": "广西现代职业技术学院",
        "partner_country": "印度",
        "partner_institution": "菲律宾南洋理工大学",
    }

    majors = ["工业机器人", "新能源汽车", "智能制造", "数字媒体"]

    for major in majors:
        config = base_config.copy()
        config['major'] = major
        config['project_name'] = f"中国-东盟{major}工匠学院"

        generator = SolutionGenerator(config)
        output_file = f"output/批量_{major}_方案.docx"
        generator.generate(output_file)
        print(f"  [OK] {major} 方案已生成")

    print(f"\n共生成 {len(majors)} 个方案文件")


def main():
    """运行所有演示"""
    print("\n" + "="*60)
    print("职业教育国际化方案生成器 - 功能演示")
    print("="*60)

    # 运行演示
    demo1_basic()
    demo2_custom()
    demo3_pricing()
    demo4_batch()

    print("\n" + "="*60)
    print("所有演示完成!")
    print("="*60)
    print("\n生成的文件位于 output/ 目录")
    print("可以用 Microsoft Word 或 WPS 打开查看和编辑\n")


if __name__ == "__main__":
    main()
