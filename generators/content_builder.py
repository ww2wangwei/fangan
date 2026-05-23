"""
内容构建器
根据输入参数动态生成方案各章节内容
"""

from typing import Dict, List
from datetime import datetime
from .ai_content_generator import AIContentGenerator


class ContentBuilder:
    """方案内容构建器"""

    def __init__(self, config: Dict):
        self.config = config
        self.school_name = config.get("school_name", "XX职业技术学院")
        self.partner_country = config.get("partner_country", "印度")
        self.partner_institution = config.get("partner_institution", "菲律宾南洋理工大学")
        self.chinese_enterprise = config.get("chinese_enterprise", "青山控股集团")
        self.major = config.get("major", "工业机器人")
        self.project_name = config.get("project_name", f"中国-{self.partner_country}关键金属产业链现代工匠学院")
        
        # 新增:建设内容选择和自定义内容
        self.selected_items = config.get("selected_items", [])
        self.custom_items = config.get("custom_items", [])
        self.excel_products = config.get("excel_products", [])
        
        # 新增:额外项目名称
        self.extra_project_names = config.get("extra_project_names", [])
        
        # 新增:AI内容生成器
        self.ai_generator = AIContentGenerator()
        self.use_ai_enhancement = config.get("use_ai_enhancement", True)

    def build_all_sections(self) -> Dict[str, str]:
        """构建所有章节内容"""
        return {
            "cover": self._build_cover(),
            "section1": self._build_section1_necessity(),
            "section2": self._build_section2_planning(),
            "section3": self._build_section3_content(),
            "section4": self._build_section4_cooperation(),
            "section5": self._build_section5_outcomes(),
            "section6": self._build_section6_budget(),
            "section7": self._build_section7_service_list(),  # 新增：第7章服务清单
        }

    def _build_cover(self) -> Dict:
        """生成封面内容"""
        current_year = datetime.now().year
        
        # 中文数字转换
        chinese_digits = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        
        # 将年份转换为中文数字（如2026 -> 二〇二六）
        year_str = str(current_year)
        chinese_year = ''.join([chinese_digits[int(digit)] for digit in year_str])
        
        # 中文月份转换
        chinese_months = ['一', '二', '三', '四', '五', '六', 
                         '七', '八', '九', '十', '十一', '十二']
        current_month = chinese_months[datetime.now().month - 1]
        
        # 构建项目名称列表（主项目 + 额外项目）
        project_names = [self.project_name]
        if self.extra_project_names:
            project_names.extend(self.extra_project_names)
        
        return {
            "logo_text": "厚国际 HOPE INTERNATIONAL",
            "school_name": self.school_name,
            "project_names": project_names,  # 支持多个项目名称
            "main_title": "建设方案",
            "reporting_unit": self.school_name,
            "cooperation_unit": self.partner_institution,
            "chinese_enterprise": self.chinese_enterprise,
            "footer_company": "厚溥海外经济合作（武汉）有限公司",
            "date": f"{chinese_year}年{current_month}月",
            "cover_image_url": self.config.get('cover_image_url', '')  # 封面图片URL
        }

    def _build_section1_necessity(self) -> Dict:
        """第一章：项目建设的必要性和可行性"""
        
        # 只使用用户自定义的内容，不自动生成任何默认内容
        custom_items = self.config.get('section1_custom_items', [])
        
        if custom_items and len(custom_items) > 0:
            # 使用用户自定义的内容
            content_list = []
            for i, item in enumerate(custom_items):
                title = item.get('title', f'第{i+1}项')
                content = item.get('content', '')
                
                # 只添加有实际内容的项（用户输入或AI生成的）
                if content and isinstance(content, str) and content.strip():
                    content_list.append({
                        "id": f"custom_{i}",
                        "subtitle": title,
                        "paragraphs": [content]
                    })
            
            # 只有当有有效内容时才返回
            if content_list:
                return {
                    "title": "第1章 项目建设的必要性和可行性",
                    "content": content_list
                }
        
        # 如果没有自定义内容，直接返回空字典（不显示第1章）
        return {}

    def _build_section2_planning(self) -> Dict:
        """第二章：项目建设规划"""
        
        # 检查是否有自定义内容
        custom_items = self.config.get('section2_custom_items', [])
        
        if custom_items and len(custom_items) > 0:
            # 使用用户自定义的内容
            content_list = []
            for i, item in enumerate(custom_items):
                title = item.get('title', f'第{i+1}项')
                content = item.get('content', '')
                
                # 只添加有实际内容的项（用户输入或AI生成的）
                if content and isinstance(content, str) and content.strip():
                    content_list.append({
                        "id": f"custom_{i}",
                        "subtitle": title,
                        "paragraphs": [content]
                    })
            
            # 只有当有有效内容时才返回
            if content_list:
                return {
                    "title": "第2章 项目建设规划",
                    "content": content_list
                }
        
        # 如果没有自定义内容，直接返回空字典（不显示第2章）
        return {}

    def _generate_generic_content(self, title: str) -> str:
        """生成通用内容（用于自定义项）"""
        return (
            f"【{title}】\n\n"
            f"基于{self.partner_country}{self.major}领域的产业发展需求，结合{self.school_name}的办学优势，"
            f"本项目具有重要的战略意义和现实价值。\n\n"
            f"一、产业背景\n"
            f"当前，全球{self.major}产业正处于快速发展阶段，{self.partner_country}作为新兴经济体，"
            f"对该领域人才需求旺盛。随着中国-{self.partner_country}产业合作的深入发展，"
            f"双方在关键矿产、新能源材料、智能制造等领域的合作项目不断增加。\n\n"
            f"二、人才需求\n"
            f"据不完全统计，{self.partner_country}{self.major}相关产业人才缺口约50万人，"
            f"急需高素质技术技能人才。特别是既懂专业技术又具备跨文化交流能力的复合型人才更为紧缺。\n\n"
            f"三、合作基础\n"
            f"{self.school_name}在{self.major}专业领域拥有丰富的教学经验和优质的教育资源，"
            f"与{self.chinese_enterprise or '多家知名企业'}保持长期合作关系。"
            f"通过引入国际标准和本土化改造，可实现专业优势的跨国输出。"
        )

    def _generate_policy_support(self) -> str:
        """生成政策支持分析"""
        return (
            f"政策红利支撑，'一带一路'教育行动提供双重保障。"
            f"国家和地方政府高度重视职业教育国际化，出台了一系列支持政策。"
            f"教育部'一带一路'教育行动专项经费支持国际化人才培养项目。"
            f"{self.partner_country}政府也将职业教育发展列为优先领域，为本项目实施提供了政策保障。"
        )

    def _generate_enterprise_support(self) -> str:
        """生成企业支持分析"""
        return (
            f"企业需求保障，龙头企业支持、人才供需两端协同发力。"
            f"青山控股、伟普新材等在{self.partner_country}投资的龙头企业对本项目给予大力支持。"
            f"这些企业不仅提供资金支持，还参与人才培养方案制定、实习实训基地建设等工作。"
            f"企业的深度参与确保了人才培养质量和就业去向。"
        )

    def _build_section3_content(self) -> Dict:
        """第三章：建设内容"""
        
        print(f"DEBUG Section3: selected_items = {len(self.selected_items)}, custom_items = {len(self.custom_items)}")
        
        # 检查是否有选择的项目或自定义项目
        if self.selected_items or self.custom_items:
            content_items = self._generate_dynamic_content()
            
            # 只有当有有效内容时才返回
            if content_items:
                print(f"DEBUG Section3: 生成 {len(content_items)} 个内容项")
                return {
                    "title": "第3章 建设内容",
                    "content": content_items
                }
        
        # 如果没有选择任何内容，直接返回空字典（不显示第3章）
        print(f"DEBUG Section3: 没有内容，返回空字典")
        return {}

    def _generate_dynamic_content(self) -> List[Dict]:
        """根据选择的产品和自定义内容生成动态建设内容"""
        content_items = []
        item_num = 1
        
        # 添加从Excel选择的产品
        for product in self.selected_items:
            subtitle = f"3.{item_num} {product.get('name', '')}"
            
            # 构建内容描述
            paragraphs = []
            desc = product.get('description', '')
            if desc:
                paragraphs.append(desc)
            
            # 添加价格和周期信息
            price = product.get('price', '0')
            unit = product.get('unit', '项')
            duration = product.get('duration', '')
            
            info_text = f"本项目内容包括{product.get('name', '')}服务，"
            if price and price != '0':
                info_text += f"预算金额为{price}{unit}。"
            if duration:
                info_text += f"实施周期为{duration}。"
            
            paragraphs.append(info_text)
            
            content_items.append({
                "subtitle": subtitle,
                "paragraphs": paragraphs
            })
            item_num += 1
        
        # 添加自定义内容
        for custom_item in self.custom_items:
            subtitle = f"3.{item_num} {custom_item.get('name', '')}"
            paragraphs = [custom_item.get('description', '')]
            
            if custom_item.get('price'):
                paragraphs.append(f"预算金额：{custom_item.get('price')}元。")
            
            content_items.append({
                "subtitle": subtitle,
                "paragraphs": paragraphs
            })
            item_num += 1
        
        return content_items

    def _build_section4_cooperation(self) -> Dict:
        """第四章：协同机制与职责矩阵"""
        
        # 检查是否有自定义内容
        custom_items = self.config.get('section4_custom_items', [])
        
        if custom_items and len(custom_items) > 0:
            # 使用用户自定义的内容
            content_list = []
            for i, item in enumerate(custom_items):
                title = item.get('title', f'第{i+1}项')
                content = item.get('content', '')
                
                # 只添加有实际内容的项（用户输入或AI生成的）
                if content and isinstance(content, str) and content.strip():
                    content_list.append({
                        "id": f"custom_{i}",
                        "subtitle": title,
                        "paragraphs": [content]
                    })
            
            # 只有当有有效内容时才返回
            if content_list:
                return {
                    "title": "第4章 协同机制与职责矩阵",
                    "content": content_list
                }
        
        # 如果没有自定义内容，直接返回空字典（不显示第4章）
        return {}

    def _build_section5_outcomes(self) -> Dict:
        """第五章：预期成果 - 根据第3章选择的产品动态生成"""
        
        print(f"DEBUG Section5: selected_items = {len(self.selected_items)}, custom_items = {len(self.custom_items)}")
        
        # 如果没有选择任何产品或自定义内容，返回空字典（不显示第5章）
        if not self.selected_items and not self.custom_items:
            print(f"DEBUG Section5: 没有选择产品，返回空字典")
            return {}
        
        # 生成预期成果表格数据
        outcomes_table = self._generate_outcomes_table()
        print(f"DEBUG Section5: 生成 {len(outcomes_table) if outcomes_table else 0} 个成果项")
        
        # 如果有从前端传递过来的完成量数据，更新表格中的完成量
        completion_data = self.config.get('section5_completion_data', {})
        if completion_data and outcomes_table:
            for index, row in enumerate(outcomes_table):
                if str(index) in completion_data:
                    row['完成量'] = float(completion_data[str(index)])
        
        # 只有当有实际成果数据时才返回
        if outcomes_table and len(outcomes_table) > 0:
            return {
                "title": "第5章 预期成果",
                "content": [
                    {
                        "id": "section5_outcomes",
                        "subtitle": "",
                        "paragraphs": [],
                        "table": outcomes_table
                    }
                ]
            }
        
        print(f"DEBUG Section5: 没有成果数据，返回空字典")
        return {}

    def _generate_outcomes_table(self) -> List[Dict]:
        """根据选择的产品生成预期成果表格"""
        outcomes = []
        
        # 定义产品名称到成果指标的映射规则
        product_outcome_map = {
            # 合作办学类
            '1+1+1': {
                '新增境外办学项目': 1,
                '在国外合作学校数': 1,
                '专业合作数量': 2,
                '在校生数': 60,
                '接收国外留学生专业数': 2,
                '接收国外留学生人数': 20,
                '签署校企合作协议及MOA协议数量': 2
            },
            '2+1': {
                '新增境外办学项目': 1,
                '在国外合作学校数': 1,
                '专业合作数量': 1,
                '在校生数': 40,
                '接收国外留学生专业数': 1,
                '接收国外留学生人数': 15,
                '签署校企合作协议及MOA协议数量': 1
            },
            
            # 标准开发类
            '国际化专业标准': {
                '国际化专业标准数量': 1,
                '资源数量(教材、在线课程)': 2
            },
            '国际化课程标准': {
                '国际化课程标准数量': 1,
                '资源数量(教材、在线课程)': 1
            },
            
            # 师资培训类
            '教师海外研修': {
                '专任教师赴国外指导和开展培训时间': 60,
                '在国外组织担任职务的专任教师人数': 8,
                '教师访学研修数量': 5,
                '教师挂职锻炼数量': 6
            },
            '企业专家来华授课': {
                '接收国外访学教师人数': 8
            },
            
            # 研讨会类
            '产教融合研讨会': {
                '承办有色金属产业链产教融合研讨会': 1,
                '培训海外院校师生及企业员工': 2000
            },
            
            # 资源建设类
            '双语教材': {
                '资源数量(教材、在线课程)': 1
            },
            '在线课程': {
                '资源数量(教材、在线课程)': 1
            }
        }
        
        # 统计各产品的数量
        product_counts = {}
        for product in self.selected_items:
            name = product.get('name', '')
            product_counts[name] = product_counts.get(name, 0) + 1
        
        # 初始化成果指标
        outcome_metrics = {
            '新增境外办学项目': 0,
            '在国外合作学校数': 0,
            '专业合作数量': 0,
            '在校生数': 0,
            '国际化专业标准数量': 0,
            '国际化课程标准数量': 0,
            '资源数量(教材、在线课程)': 0,
            '接收国外留学生专业数': 0,
            '接收国外留学生人数': 0,
            '接收国外访学教师人数': 0,
            '专任教师赴国外指导和开展培训时间': 0,
            '在国外组织担任职务的专任教师人数': 0,
            '承办有色金属产业链产教融合研讨会': 0,
            '培训海外院校师生及企业员工': 0,
            '签署校企合作协议及MOA协议数量': 0,
            '教师访学研修数量': 0,
            '教师挂职锻炼数量': 0
        }
        
        # 根据选择的产品累加成果 - 使用部分匹配
        for product_name, count in product_counts.items():
            matched = False
            for key, metrics in product_outcome_map.items():
                if product_name.startswith(key) or key in product_name:
                    matched = True
                    for metric, value in metrics.items():
                        if metric in outcome_metrics:
                            outcome_metrics[metric] += value * count
                    break
            if not matched:
                print(f'Warning: Product "{product_name}" not matched in product_outcome_map')
        
        # 定义固定的17行模板（序号、项目内容、单位）
        fixed_rows = [
            {'序号': 1, '项目内容': '新增境外办学项目', '单位': '个'},
            {'序号': 2, '项目内容': '在国外合作学校数', '单位': '所'},
            {'序号': 3, '项目内容': '专业合作数量', '单位': '个'},
            {'序号': 4, '项目内容': '在校生数', '单位': '人'},
            {'序号': 5, '项目内容': '国际化专业标准数量', '单位': '个'},
            {'序号': 6, '项目内容': '国际化课程标准数量', '单位': '个'},
            {'序号': 7, '项目内容': '资源数量（教材、在线课程）', '单位': '个'},
            {'序号': 8, '项目内容': '接收国外留学生专业数', '单位': '个'},
            {'序号': 9, '项目内容': '接收国外留学生人数', '单位': '人'},
            {'序号': 10, '项目内容': '接收国外访学教师人数', '单位': '人'},
            {'序号': 11, '项目内容': '专任教师赴国外指导和开展培训时间', '单位': '人日'},
            {'序号': 12, '项目内容': '在国外组织担任职务的专任教师人数', '单位': '人'},
            {'序号': 13, '项目内容': '承办有色金属产业链产教融合研讨会', '单位': '场'},
            {'序号': 14, '项目内容': '培训海外院校师生及企业员工', '单位': '人次'},
            {'序号': 15, '项目内容': '签署校企合作协议及MOA协议数量', '单位': '份'},
            {'序号': 16, '项目内容': '教师访学研修数量', '单位': '人'},
            {'序号': 17, '项目内容': '教师挂职锻炼数量', '单位': '人'}
        ]
        
        # 构建完整的表格数据，只有完成量是动态计算的
        outcomes = []
        for row_template in fixed_rows:
            item_content = row_template['项目内容']
            # 查找对应的指标值
            completion_value = outcome_metrics.get(item_content, 0)
            
            outcomes.append({
                '序号': row_template['序号'],
                '项目内容': item_content,
                '单位': row_template['单位'],
                '完成量': completion_value
            })
        
        return outcomes

    def _build_section6_budget(self) -> Dict:
        """第六章：项目保障 - 自定义内容"""
        
        # 检查是否有自定义内容
        custom_items = self.config.get('section6_custom_items', [])
        
        if custom_items and len(custom_items) > 0:
            # 使用用户自定义的内容
            content_list = []
            for i, item in enumerate(custom_items):
                title = item.get('title', f'第{i+1}项')
                content = item.get('content', '')
                
                # 只添加有实际内容的项（用户输入或AI生成的）
                if content and isinstance(content, str) and content.strip():
                    content_list.append({
                        "id": f"custom_{i}",
                        "subtitle": title,
                        "paragraphs": [content]
                    })
            
            # 只有当有有效内容时才返回
            if content_list:
                return {
                    "title": "第6章 项目保障",
                    "content": content_list
                }
        
        # 如果没有自定义内容，直接返回空字典（不显示第6章）
        return {}

    def _build_section7_service_list(self) -> Dict:
        """第七章：服务清单 - 根据选择的产品生成详细的服务清单表格"""
        
        # 优先使用从前端传递过来的服务清单数据（如果有的话）
        service_list_from_frontend = self.config.get('section7_service_list', [])
        if service_list_from_frontend and len(service_list_from_frontend) > 0:
            # 使用用户在前端编辑的数据
            return {
                "title": "第7章 服务清单",
                "content": [
                    {
                        "id": "section7_service_list",
                        "subtitle": "",
                        "paragraphs": [],
                        "table": service_list_from_frontend
                    }
                ]
            }
        
        # 如果没有前端数据，则根据选择的产品自动生成
        if not self.selected_items and not self.custom_items:
            return {}
        
        # 生成服务清单表格数据
        service_table = self._generate_service_list_table()
        
        # 只有当有实际服务数据时才返回
        if service_table and len(service_table) > 0:
            return {
                "title": "第7章 服务清单",
                "content": [
                    {
                        "id": "section7_service_list",
                        "subtitle": "",
                        "paragraphs": [],
                        "table": service_table
                    }
                ]
            }
        
        return {}

    def _generate_service_list_table(self) -> List[Dict]:
        """根据选择的产品生成服务清单表格"""
        services = []
        row_num = 1
        
        # 定义服务清单模板 - 根据产品名称映射到对应的服务内容
        service_template_map = {
            '海外院校对接': {
                '一级项目': '海外机构建设全流程',
                '二级任务项': '海外院校资源开发',
                '服务内容': [
                    '1. 海外院校资源库建设与筛选',
                    '2. 海外院校合作政策与需求调研',
                    '3. 海外院校联络与合作意向确认',
                    '4. 合作模式与实施方案设计',
                    '5. 项目材料准备与立项申请支持',
                    '6. 合作项目启动与执行支持',
                    '7. 合作后的年度评估与关系维护'
                ],
                '说明': '与乌兹别克斯坦国立理工学院、华友钴业、中伟新材料印尼基地深度对接，完成1所海外院校、双方学校"1+1+1"主管部门备案'
            },
            '中资企业对接': {
                '一级项目': '海外机构建设全流程',
                '二级任务项': '中资企业对接',
                '服务内容': [
                    '1. 合作模式设计（就业、实习、工坊等）',
                    '2. 企业拜访与对接活动组织',
                    '3. 合作内容规划与方案设计',
                    '4. 协议草案与商务谈判支持',
                    '5. 项目实施路径设计',
                    '6. 项目启动与执行协调',
                    '7. 后期运营评估与合作深化建议'
                ],
                '说明': '1企业合作协议签约'
            },
            '出访交流': {
                '一级项目': '服务',
                '二级任务项': '中方领导赴印尼学校企业及签约挂牌',
                '服务内容': [
                    '1. 来访需求调研与访问目标确认',
                    '2. 访问行程与议程设计（中英双语）',
                    '3. 访问所需材料准备与宣传支持',
                    '4. 会议组织与教学观摩安排',
                    '5. 校园参观、企业参访与成果展示活动策划',
                    '6. 差旅与接待服务（酒店/交通/餐饮）',
                    '7. 全程口译与文件翻译',
                    '8. 文化体验与企业/产业园区考察（可选）',
                    '9. 签约仪式与合影/媒体宣传服务',
                    '10. 访问后总结与合作推进支持'
                ],
                '说明': '3名中方领导期间的出行服务、学校、企业交流及挂牌仪式整体时间安排、实施安排（可以单独出来）'
            }
        }
        
        # 遍历选中的产品，生成服务清单
        for product in self.selected_items:
            product_name = product.get('name', '')
            
            # 查找匹配的服务模板 - 使用更宽松的匹配策略
            matched_template = None
            matched_key = None
            
            for key, template in service_template_map.items():
                # 检查产品名称是否包含关键词，或者关键词是否包含在产品名称中
                if key in product_name or product_name in key or product_name.startswith(key):
                    matched_template = template
                    matched_key = key
                    break
            
            # 如果找到匹配的模板，添加到服务清单
            if matched_template:
                service_content_str = '\n'.join(matched_template['服务内容'])
                
                services.append({
                    '序号': row_num,
                    '一级项目': matched_template['一级项目'],
                    '二级任务项': matched_template['二级任务项'],
                    '服务内容': service_content_str,
                    '说明': '',  # 说明列留空，由用户自行填写
                    '费用': product.get('price', '0')
                })
                row_num += 1
            else:
                # 如果没有匹配的模板，使用通用格式生成一行
                services.append({
                    '序号': row_num,
                    '一级项目': '服务项目',
                    '二级任务项': product_name,
                    '服务内容': product.get('service_content', '') if product.get('service_content') else f'提供{product_name}相关服务',
                    '说明': '',
                    '费用': product.get('price', '0')
                })
                row_num += 1
        
        # 添加自定义项目的服务清单
        for custom_item in self.custom_items:
            item_name = custom_item.get('name', '')
            item_desc = custom_item.get('description', '')
            item_price = custom_item.get('price', '0')
            
            services.append({
                '序号': row_num,
                '一级项目': '自定义项目',
                '二级任务项': item_name,
                '服务内容': item_desc if item_desc else '根据客户需求定制服务内容',
                '说明': '',  # 说明列留空，由用户自行填写
                '费用': str(item_price)
            })
            row_num += 1
        
        return services

    def _generate_budget_items(self) -> List[Dict]:
        """生成预算明细 - 基于Excel报价单和选择的项目"""
        budget_items = []
        
        # 如果有选择的产品,使用实际价格
        if self.selected_items:
            for idx, product in enumerate(self.selected_items, 1):
                try:
                    price_str = product.get('price', '0')
                    # 尝试解析价格(可能是数字或字符串)
                    if isinstance(price_str, str):
                        # 清理价格字符串,提取数字
                        import re
                        numbers = re.findall(r'[\d,]+\.?\d*', price_str)
                        price = float(numbers[0].replace(',', '')) if numbers else 0
                    else:
                        price = float(price_str)
                    
                    quantity = 1
                    unit = product.get('unit', '项')
                    
                    budget_items.append({
                        "item": product.get('name', f'项目{idx}'),
                        "quantity": quantity,
                        "unit": unit,
                        "price": price,
                        "amount": price * quantity
                    })
                except (ValueError, TypeError) as e:
                    print(f"价格解析错误: {e}, 产品: {product}")
        
        # 添加自定义项目的预算
        if self.custom_items:
            for custom_item in self.custom_items:
                try:
                    price = float(custom_item.get('price', 0))
                    budget_items.append({
                        "item": custom_item.get('name', ''),
                        "quantity": 1,
                        "unit": "项",
                        "price": price,
                        "amount": price
                    })
                except (ValueError, TypeError):
                    continue
        
        # 如果没有选择任何项目,使用默认预算模板
        if not budget_items:
            budget_items = [
                {"item": "海外院校对接服务", "quantity": 1, "unit": "项", "price": 50000, "amount": 50000},
                {"item": "专业标准开发认证", "quantity": 2, "unit": "个", "price": 30000, "amount": 60000},
                {"item": "课程标准开发认证", "quantity": 3, "unit": "门", "price": 15000, "amount": 45000},
                {"item": "开工仪式策划执行", "quantity": 1, "unit": "场", "price": 60000, "amount": 60000},
                {"item": "海外教学场所建设", "quantity": 1, "unit": "项", "price": 50000, "amount": 50000},
                {"item": "出访交流(4天3夜)", "quantity": 3, "unit": "人次", "price": 40000, "amount": 120000},
                {"item": "来华留学服务", "quantity": 5, "unit": "人", "price": 20000, "amount": 100000},
                {"item": "视频资源制作", "quantity": 10, "unit": "分钟", "price": 2000, "amount": 20000},
                {"item": "师资培训", "quantity": 1, "unit": "项", "price": 80000, "amount": 80000},
                {"item": "项目管理费", "quantity": 1, "unit": "项", "price": 50000, "amount": 50000},
            ]
        
        return budget_items


def main():
    """测试内容构建器"""
    config = {
        "school_name": "广西现代职业技术学院",
        "partner_country": "印度",
        "partner_institution": "菲律宾南洋理工大学",
        "major": "工业机器人",
        "project_name": "中国-东盟工业机器人工匠学院",
    }

    builder = ContentBuilder(config)
    sections = builder.build_all_sections()

    for key, section in sections.items():
        print(f"\n{'='*60}")
        print(f"{key}:")
        if isinstance(section, dict):
            print(f"标题: {section.get('title', '')}")
            if 'content' in section:
                print(f"子章节数: {len(section['content'])}")
        else:
            print(str(section)[:200])


if __name__ == "__main__":
    main()
