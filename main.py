"""
职业教育国际化方案生成器 - 主程序
"""

import sys
import os
import argparse
from typing import Dict

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import DEFAULT_CONFIG, EXCEL_FILE
from parsers.excel_parser import ExcelParser
from generators.content_builder import ContentBuilder
from generators.doc_generator import DocGenerator


class SolutionGenerator:
    """方案生成器主类"""

    def __init__(self, config: Dict = None):
        self.config = config or DEFAULT_CONFIG.copy()
        self.excel_data = None

    def load_pricing_data(self, excel_file: str = None):
        """加载报价单数据"""
        file_path = excel_file or EXCEL_FILE
        try:
            parser = ExcelParser(file_path)
            self.excel_data = parser.parse_all()
            print(f"[OK] 成功加载报价单数据")
            return True
        except Exception as e:
            print(f"✗ 加载报价单失败: {e}")
            return False

    def generate(self, output_path: str = None) -> str:
        """生成方案文档"""
        print("\n开始生成方案...")

        # 构建内容
        builder = ContentBuilder(self.config)
        sections = builder.build_all_sections()

        # 生成文档
        if output_path is None:
            school_short = self.config.get("school_name", "学校")[:8]
            output_path = f"output/{school_short}_{self.config.get('major', '专业')}_建设方案.docx"

        generator = DocGenerator(output_path)
        result_file = generator.generate(sections)

        print(f"[OK] 方案已生成: {result_file}")
        return result_file

    def update_config(self, **kwargs):
        """更新配置"""
        self.config.update(kwargs)

    def print_config(self):
        """打印当前配置"""
        print("\n" + "="*60)
        print("当前配置:")
        print("="*60)
        for key, value in self.config.items():
            print(f"  {key}: {value}")
        print("="*60 + "\n")


def interactive_mode():
    """交互模式"""
    print("\n" + "="*60)
    print("职业教育国际化方案生成器")
    print("="*60)
    print("\n请回答以下问题以生成定制化方案:\n")

    # 收集用户输入
    config = {}

    school_name = input(f"1. 学校名称 [{DEFAULT_CONFIG['school_name']}]: ").strip()
    config['school_name'] = school_name or DEFAULT_CONFIG['school_name']

    country = input(f"2. 合作国家/地区 [{DEFAULT_CONFIG['partner_country']}]: ").strip()
    config['partner_country'] = country or DEFAULT_CONFIG['partner_country']

    institution = input(f"3. 合作院校 [{DEFAULT_CONFIG['partner_institution']}]: ").strip()
    config['partner_institution'] = institution or DEFAULT_CONFIG['partner_institution']

    enterprise = input(f"4. 中资企业名称 [{DEFAULT_CONFIG.get('chinese_enterprise', '')}]: ").strip()
    config['chinese_enterprise'] = enterprise or DEFAULT_CONFIG.get('chinese_enterprise', '')

    major = input(f"5. 专业方向 [{DEFAULT_CONFIG['major']}]: ").strip()
    config['major'] = major or DEFAULT_CONFIG['major']

    project_name = input(f"6. 项目名称 [中国-{config['partner_country']}{major}工匠学院]: ").strip()
    if not project_name:
        project_name = f"中国-{config['partner_country']}{major}工匠学院"
    config['project_name'] = project_name

    # 显示配置
    generator = SolutionGenerator(config)
    generator.print_config()

    confirm = input("确认生成方案? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消生成。")
        return

    # 尝试加载报价单
    generator.load_pricing_data()

    # 生成方案
    output = input(f"\n输出文件路径 [output/{config['school_name'][:8]}_{config['major']}_建设方案.docx]: ").strip()
    output_path = output if output else None

    generator.generate(output_path)

    print("\n[OK] 方案生成完成！")


def cli_mode(args):
    """命令行模式"""
    config = DEFAULT_CONFIG.copy()

    if args.school:
        config['school_name'] = args.school
    if args.country:
        config['partner_country'] = args.country
    if args.institution:
        config['partner_institution'] = args.institution
    if args.major:
        config['major'] = args.major
    if args.project:
        config['project_name'] = args.project

    generator = SolutionGenerator(config)
    generator.print_config()

    # 加载报价单
    if args.pricing:
        generator.load_pricing_data(args.pricing)

    # 生成方案
    output_path = args.output if args.output else None
    generator.generate(output_path)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='职业教育国际化方案生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  交互模式:
    python main.py --interactive

  命令行模式:
    python main.py --school "广西现代职业技术学院" --country "印度" --major "工业机器人"
    python main.py --school "XX职院" --output "我的方案.docx"
        """
    )

    parser.add_argument('-i', '--interactive', action='store_true',
                       help='进入交互模式')
    parser.add_argument('-s', '--school', type=str,
                       help='学校名称')
    parser.add_argument('-c', '--country', type=str,
                       help='合作国家/地区')
    parser.add_argument('-inst', '--institution', type=str,
                       help='合作院校')
    parser.add_argument('-m', '--major', type=str,
                       help='专业方向')
    parser.add_argument('-p', '--project', type=str,
                       help='项目名称')
    parser.add_argument('-o', '--output', type=str,
                       help='输出文件路径')
    parser.add_argument('--pricing', type=str,
                       help='报价单Excel文件路径')

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
    else:
        cli_mode(args)


if __name__ == "__main__":
    main()
