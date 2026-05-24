"""
Word文档生成器
使用python-docx生成格式化的建设方案文档
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from typing import Dict, List
import os


class DocGenerator:
    """Word文档生成器"""

    def __init__(self, output_path: str = "output/建设方案.docx"):
        self.output_path = output_path
        self.doc = Document()
        self._setup_styles()

    def _setup_styles(self):
        """设置文档样式"""
        # 设置默认字体
        style = self.doc.styles['Normal']
        font = style.font
        font.name = '宋体'
        font.size = Pt(12)
        font.color.rgb = RGBColor(0, 0, 0)

        # 中文字体设置
        element = style.element
        rPr = element.find('.//w:rPr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        if rPr is not None:
            rFonts = rPr.find('.//w:rFonts', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
            if rFonts is not None:
                rFonts.set(qn('w:eastAsia'), '宋体')
        
        # 设置段落行距和间距
        style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        style.paragraph_format.space_before = Pt(0)
        style.paragraph_format.space_after = Pt(6)
        
        # 创建标题样式
        self._create_heading_styles()
    
    def _create_heading_styles(self):
        """创建标题样式"""
        # 一级标题（章标题）
        heading1_style = self.doc.styles.add_style('Heading1Custom', 1)  # Paragraph style
        heading1_font = heading1_style.font
        heading1_font.name = '黑体'
        heading1_font.size = Pt(16)
        heading1_font.bold = True
        heading1_font.color.rgb = RGBColor(0, 51, 102)  # 深蓝色
        
        heading1_element = heading1_style.element
        rPr = heading1_element.find('.//w:rPr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        if rPr is not None:
            rFonts = rPr.find('.//w:rFonts', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
            if rFonts is not None:
                rFonts.set(qn('w:eastAsia'), '黑体')
        
        heading1_style.paragraph_format.space_before = Pt(18)
        heading1_style.paragraph_format.space_after = Pt(12)
        heading1_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        
        # 二级标题（节标题）
        heading2_style = self.doc.styles.add_style('Heading2Custom', 1)
        heading2_font = heading2_style.font
        heading2_font.name = '黑体'
        heading2_font.size = Pt(14)
        heading2_font.bold = True
        heading2_font.color.rgb = RGBColor(51, 102, 153)  # 中蓝色
        
        heading2_element = heading2_style.element
        rPr = heading2_element.find('.//w:rPr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        if rPr is not None:
            rFonts = rPr.find('.//w:rFonts', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
            if rFonts is not None:
                rFonts.set(qn('w:eastAsia'), '黑体')
        
        heading2_style.paragraph_format.space_before = Pt(12)
        heading2_style.paragraph_format.space_after = Pt(6)
        heading2_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        
        # 三级标题
        heading3_style = self.doc.styles.add_style('Heading3Custom', 1)
        heading3_font = heading3_style.font
        heading3_font.name = '黑体'
        heading3_font.size = Pt(12)
        heading3_font.bold = True
        heading3_font.color.rgb = RGBColor(79, 129, 189)  # 浅蓝色
        
        heading3_element = heading3_style.element
        rPr = heading3_element.find('.//w:rPr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        if rPr is not None:
            rFonts = rPr.find('.//w:rFonts', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
            if rFonts is not None:
                rFonts.set(qn('w:eastAsia'), '黑体')
        
        heading3_style.paragraph_format.space_before = Pt(10)
        heading3_style.paragraph_format.space_after = Pt(4)
        heading3_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    def add_cover(self, content):
        """添加封面"""
        # 如果content是字典，需要从中提取信息构建封面
        if isinstance(content, dict):
            # 从字典中提取封面信息
            school_name = content.get('school_name', '')
            project_names = content.get('project_names', [])
            main_title = content.get('main_title', '建设方案')
            reporting_unit = content.get('reporting_unit', '')
            cooperation_unit = content.get('cooperation_unit', '')
            chinese_enterprise = content.get('chinese_enterprise', '')
            footer_company = content.get('footer_company', '')
            date = content.get('date', '')
            cover_image_url = content.get('cover_image_url', '')

            # 添加空行使内容居中
            for _ in range(6):
                p = self.doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 添加Logo文字
            logo_text = content.get('logo_text', '')
            if logo_text:
                p = self.doc.add_paragraph(logo_text)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(14)
                run.font.name = 'Arial'
                run.font.color.rgb = RGBColor(100, 100, 100)

            # 添加空行
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 添加学校名称
            if school_name:
                p = self.doc.add_paragraph(school_name)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(18)
                run.font.bold = True
                run.font.name = '黑体'

            # 添加空行
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 添加项目名称（支持多个）
            for project_name in project_names:
                p = self.doc.add_paragraph(project_name)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(22)
                run.font.bold = True
                run.font.name = '黑体'

            # 添加主标题
            if main_title:
                p = self.doc.add_paragraph(main_title)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(22)
                run.font.bold = True
                run.font.name = '黑体'

            # 添加空行
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 添加申报单位等信息
            if reporting_unit:
                p = self.doc.add_paragraph(f"申报单位：{reporting_unit}")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(14)
                run.font.name = '宋体'

            if cooperation_unit:
                p = self.doc.add_paragraph(f"合作单位：{cooperation_unit}")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(14)
                run.font.name = '宋体'

            if chinese_enterprise:
                p = self.doc.add_paragraph(f"中资企业：{chinese_enterprise}")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(14)
                run.font.name = '宋体'

            # 添加空行
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 添加日期
            if date:
                p = self.doc.add_paragraph(date)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(14)
                run.font.name = '宋体'

            # 添加底部公司
            if footer_company:
                p = self.doc.add_paragraph(footer_company)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.runs[0]
                run.font.size = Pt(12)
                run.font.name = '宋体'
        else:
            # 如果content是字符串，按原有逻辑处理
            # 添加空行使内容居中
            for _ in range(8):
                p = self.doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 添加标题
            lines = content.strip().split('\n')
            for i, line in enumerate(lines):
                if line.strip():  # 跳过空行
                    p = self.doc.add_paragraph(line)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

                    run = p.runs[0]
                    if i == 0:  # 项目名称
                        run.font.size = Pt(22)
                        run.font.bold = True
                        run.font.name = '黑体'
                    else:
                        run.font.size = Pt(16)
                        run.font.name = '宋体'

        # 添加分页符
        self.doc.add_page_break()

    def add_section(self, section_data: Dict):
        """添加章节"""
        try:
            # 检查是否是空字典
            if not section_data or len(section_data) == 0:
                return
            
            # 添加章节标题
            if 'title' in section_data:
                p = self.doc.add_paragraph(section_data['title'])
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = p.runs[0]
                run.font.size = Pt(16)
                run.font.bold = True
                run.font.name = '黑体'

                # 添加段后间距
                p.paragraph_format.space_after = Pt(12)

            # 添加内容
            if 'content' in section_data and section_data['content']:
                for subsection in section_data['content']:
                    # 检查subsection是否是有效的字典
                    if not subsection or not isinstance(subsection, dict):
                        continue
                    
                    # 添加子标题
                    if 'subtitle' in subsection and subsection['subtitle']:
                        p = self.doc.add_paragraph(subsection['subtitle'])
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        run = p.runs[0]
                        run.font.size = Pt(14)
                        run.font.bold = True
                        run.font.name = '黑体'
                        p.paragraph_format.space_before = Pt(12)
                        p.paragraph_format.space_after = Pt(6)

                    # 添加段落
                    if 'paragraphs' in subsection and subsection['paragraphs']:
                        for para_text in subsection['paragraphs']:
                            if isinstance(para_text, str):
                                text = para_text
                            else:
                                text = str(para_text)
                            
                            # 清理多余的换行符，让内容在Word中自动换行
                            import re
                            # 将所有换行符（包括\r\n和\n）替换为空格
                            text = re.sub(r'[\r\n]+', ' ', text)
                            # 清理多余的空格
                            text = re.sub(r'\s+', ' ', text).strip()
                            
                            p = self.doc.add_paragraph(text)
                            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
                            
                            run = p.runs[0]
                            run.font.size = Pt(12)
                            run.font.name = '宋体'
                            
                            # 检查是否为列表项（以数字+点开头）或"职责："标签
                            is_list_item = bool(re.match(r'^\d+\.\s', text.strip()))
                            is_label = text.strip() in ['职责：', '职责:', '职责']
                            
                            # "职责："标签左对齐，无缩进
                            if is_label:
                                p.paragraph_format.first_line_indent = Pt(0)
                                p.paragraph_format.left_indent = Pt(0)
                            # 列表项使用悬挂缩进
                            elif is_list_item:
                                p.paragraph_format.first_line_indent = Pt(0)
                                p.paragraph_format.left_indent = Pt(24)
                            # 其他段落使用首行缩进
                            else:
                                p.paragraph_format.first_line_indent = Pt(24)

            # 添加预算表格
            if 'budget_items' in section_data and section_data['budget_items']:
                self._add_budget_table(section_data['budget_items'])

            # 添加内容中的表格（如第5章预期成果、第7章服务清单）
            if 'content' in section_data and section_data['content']:
                for subsection in section_data['content']:
                    if not subsection or not isinstance(subsection, dict):
                        continue
                    if 'table' in subsection and subsection['table']:
                        # 判断是哪种类型的表格
                        table_data = subsection['table']
                        if len(table_data) > 0:
                            first_row = table_data[0]
                            # 如果包含"完成量"字段，则是预期成果表格
                            if '完成量' in first_row:
                                self._add_outcomes_table(table_data)
                            else:
                                # 否则是服务清单表格
                                self._add_service_list_table(table_data)
        
        except Exception as e:
            import traceback
            print(f"添加章节时出错: {e}")
            traceback.print_exc()
            # 添加错误提示
            p = self.doc.add_paragraph(f"章节内容生成错误: {str(e)}")
            p.runs[0].font.color.rgb = RGBColor(255, 0, 0)

    def _add_budget_table(self, budget_items: List[Dict]):
        """添加预算表格"""
        # 添加表格标题
        p = self.doc.add_paragraph("表6-1 项目预算明细表")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.size = Pt(12)
        run.font.bold = True

        # 创建表格
        table = self.doc.add_table(rows=len(budget_items) + 1, cols=5)
        table.style = 'Table Grid'

        # 设置表头
        headers = ["序号", "项目名称", "数量", "单价(元)", "金额(元)"]
        for i, header in enumerate(headers):
            cell = table.rows[0].cells[i]
            cell.text = header
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = cell.paragraphs[0].runs[0]
            run.font.bold = True
            run.font.size = Pt(10)

        # 填充数据
        total_amount = 0
        for i, item in enumerate(budget_items, 1):
            row = table.rows[i]
            row.cells[0].text = str(i)
            row.cells[1].text = item.get('item', '')
            row.cells[2].text = str(item.get('quantity', ''))
            row.cells[3].text = f"{item.get('price', 0):,.0f}"
            amount = item.get('quantity', 0) * item.get('price', 0)
            row.cells[4].text = f"{amount:,.0f}"
            total_amount += amount

            # 居中对齐
            for cell in row.cells:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 添加合计行
        total_row = table.add_row()
        total_row.cells[0].text = "合计"
        total_row.cells[0].merge(total_row.cells[2])
        total_row.cells[3].text = f"{total_amount:,.0f}"
        total_row.cells[3].merge(total_row.cells[4])

        for cell in total_row.cells:
            run = cell.paragraphs[0].runs[0]
            run.font.bold = True

        # 添加总计说明
        p = self.doc.add_paragraph(f"项目总投资：人民币 {total_amount:,.0f} 元（大写：{self._number_to_chinese(total_amount)}）")
        p.paragraph_format.first_line_indent = Pt(24)
        run = p.runs[0]
        run.font.size = Pt(12)

    def _number_to_chinese(self, num: int) -> str:
        """将数字转换为中文大写"""
        chinese_nums = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
        chinese_units = ['', '拾', '佰', '仟']
        chinese_big_units = ['', '万', '亿']

        # 确保是整数
        num = int(num)

        if num == 0:
            return "零元整"

        result = ""
        unit_idx = 0

        while num > 0:
            section = num % 10000
            num //= 10000

            if section > 0:
                section_str = ""
                section_unit_idx = 0

                while section > 0:
                    digit = int(section % 10)
                    section //= 10

                    if digit > 0:
                        section_str = chinese_nums[digit] + chinese_units[section_unit_idx] + section_str
                    elif section_str and section_str[0] != '零':
                        section_str = '零' + section_str

                    section_unit_idx += 1

                result = section_str + chinese_big_units[unit_idx] + result

            unit_idx += 1

        return result + "元整"

    def _add_outcomes_table(self, table_data: List[Dict]):
        """添加预期成果表格（第5章）"""
        if not table_data or len(table_data) == 0:
            return
        
        try:
            # 添加表格标题
            p = self.doc.add_paragraph("表5-1 预期成果")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.font.size = Pt(12)
            run.font.bold = True

            # 预期成果的列：序号、项目内容、单位、完成量
            cols = 4
            
            # 创建表格（+1为表头行）
            table = self.doc.add_table(rows=len(table_data) + 1, cols=cols)
            table.style = 'Table Grid'

            # 设置表头
            headers = ["序号", "项目内容", "单位", "完成量"]
            for i, header in enumerate(headers):
                cell = table.rows[0].cells[i]
                cell.text = header
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = cell.paragraphs[0].runs[0]
                run.font.bold = True
                run.font.size = Pt(10)

            # 填充数据
            for i, row_data in enumerate(table_data, 1):
                row = table.rows[i]
                
                # 确保每个字段都存在
                seq_no = str(row_data.get('序号', i))
                project_content = str(row_data.get('项目内容', ''))
                unit = str(row_data.get('单位', ''))
                completion = str(row_data.get('完成量', ''))
                
                # 填充单元格
                row.cells[0].text = seq_no
                row.cells[1].text = project_content
                row.cells[2].text = unit
                row.cells[3].text = completion

                # 设置字体大小
                for cell in row.cells:
                    run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.add_run()
                    run.font.size = Pt(9)
                
                # 居中对齐序号和完成量
                row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        except Exception as e:
            import traceback
            print(f"生成预期成果表格时出错: {e}")
            traceback.print_exc()
            # 如果生成表格失败，至少添加一个提示
            p = self.doc.add_paragraph(f"预期成果数据格式错误: {str(e)}")
            p.runs[0].font.color.rgb = RGBColor(255, 0, 0)

    def _add_service_list_table(self, table_data: List[Dict]):
        """添加服务清单表格"""
        if not table_data or len(table_data) == 0:
            return
        
        try:
            # 添加表格标题
            p = self.doc.add_paragraph("表7-1 服务清单")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.font.size = Pt(12)
            run.font.bold = True

            # 服务清单的列：序号、一级项目、二级任务项、服务内容、说明、费用
            cols = 6
            
            # 创建表格（+1为表头行，+1为总计行）
            table = self.doc.add_table(rows=len(table_data) + 2, cols=cols)
            table.style = 'Table Grid'

            # 设置表头
            headers = ["序号", "一级项目", "二级任务项", "服务内容", "说明", "费用"]
            for i, header in enumerate(headers):
                cell = table.rows[0].cells[i]
                cell.text = header
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = cell.paragraphs[0].runs[0]
                run.font.bold = True
                run.font.size = Pt(10)

            # 填充数据
            total_fee = 0
            for i, row_data in enumerate(table_data, 1):
                row = table.rows[i]
                
                # 确保每个字段都存在
                seq_no = str(row_data.get('序号', i))
                level1 = str(row_data.get('一级项目', ''))
                level2 = str(row_data.get('二级任务项', ''))
                service_content = row_data.get('服务内容', '')
                if isinstance(service_content, list):
                    service_content = '\n'.join(service_content)
                service_content = str(service_content)
                description = str(row_data.get('说明', ''))
                fee_str = str(row_data.get('费用', '0'))
                
                # 填充单元格
                row.cells[0].text = seq_no
                row.cells[1].text = level1
                row.cells[2].text = level2
                row.cells[3].text = service_content
                row.cells[4].text = description
                row.cells[5].text = fee_str

                # 设置字体大小
                for cell in row.cells:
                    run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.add_run()
                    run.font.size = Pt(9)
                
                # 计算总费用
                try:
                    fee_num = float(''.join(filter(lambda c: c.isdigit() or c == '.', fee_str)))
                    total_fee += fee_num
                except (ValueError, TypeError):
                    pass

            # 添加合计行
            total_row = table.rows[len(table_data) + 1]
            total_row.cells[0].text = "合计"
            total_row.cells[0].merge(total_row.cells[4])
            total_row.cells[5].text = f"{total_fee:.2f}万元" if total_fee > 0 else "0万元"
            
            for cell in total_row.cells:
                run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.add_run()
                run.font.bold = True
                run.font.size = Pt(10)
        
        except Exception as e:
            import traceback
            print(f"生成服务清单表格时出错: {e}")
            traceback.print_exc()
            # 如果生成表格失败，至少添加一个提示
            p = self.doc.add_paragraph(f"服务清单数据格式错误: {str(e)}")
            p.runs[0].font.color.rgb = RGBColor(255, 0, 0)

    def add_table_of_contents(self):
        """添加目录占位符"""
        p = self.doc.add_paragraph("目录")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.size = Pt(16)
        run.font.bold = True

        self.doc.add_paragraph("\n（此处为目录占位符，请在Word中使用'引用->目录'功能生成正式目录）\n")
        self.doc.add_page_break()

    def generate(self, sections: Dict) -> str:
        """生成完整文档"""
        # 添加封面
        if 'cover' in sections:
            self.add_cover(sections['cover'])

        # 添加目录
        self.add_table_of_contents()

        # 添加各章节
        section_keys = ['section1', 'section2', 'section3', 'section4',
                       'section5', 'section6', 'section7']

        is_first_section = True
        for key in section_keys:
            if key in sections and sections[key]:
                # 如果不是第一章，在新章节前添加分页符
                if not is_first_section:
                    self.doc.add_page_break()
                self.add_section(sections[key])
                is_first_section = False

        # 保存文档
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.doc.save(self.output_path)

        return self.output_path


def main():
    """测试文档生成器"""
    from generators.content_builder import ContentBuilder

    config = {
        "school_name": "广西现代职业技术学院",
        "partner_country": "印度",
        "partner_institution": "菲律宾南洋理工大学",
        "major": "工业机器人",
        "project_name": "中国-东盟工业机器人工匠学院",
    }

    builder = ContentBuilder(config)
    sections = builder.build_all_sections()

    generator = DocGenerator("output/测试方案.docx")
    output_file = generator.generate(sections)

    print(f"文档已生成: {output_file}")


if __name__ == "__main__":
    main()
