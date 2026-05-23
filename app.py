"""
方案生成器 - 简单Web界面
使用Flask提供Web服务
"""

import sys
import os
import json
from flask import Flask, render_template, request, send_file, jsonify
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import SolutionGenerator
from config.settings import DEFAULT_CONFIG
from parsers.excel_parser import ExcelParser

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'output'
app.config['COVER_IMAGES_FOLDER'] = 'uploads'
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大上传16MB

# 确保目录存在
os.makedirs('output', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
os.makedirs('static', exist_ok=True)

# 全局Excel解析器实例
excel_parser = None


def get_excel_parser():
    """获取Excel解析器单例"""
    global excel_parser
    if excel_parser is None:
        try:
            excel_parser = ExcelParser("厚溥国际职业教育国际化产品报价单2026版(2.0).xlsx")
            excel_parser.parse_all()
        except Exception as e:
            print(f"加载Excel失败: {e}")
            return None
    return excel_parser


@app.route('/')
def index():
    """首页"""
    return render_template('index.html', defaults=DEFAULT_CONFIG)


@app.route('/api/products')
def get_products():
    """API: 获取所有可选产品列表"""
    try:
        parser = get_excel_parser()
        if parser:
            products = parser.get_all_products_for_selection()
            return jsonify(products)
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate', methods=['POST'])
def generate():
    """生成方案"""
    try:
        # 获取表单数据
        config = {
            'school_name': request.form.get('school_name', DEFAULT_CONFIG['school_name']),
            'partner_country': request.form.get('partner_country', DEFAULT_CONFIG['partner_country']),
            'partner_institution': request.form.get('partner_institution', DEFAULT_CONFIG['partner_institution']),
            'chinese_enterprise': request.form.get('chinese_enterprise', DEFAULT_CONFIG.get('chinese_enterprise', '')),
            'major': request.form.get('major', DEFAULT_CONFIG['major']),
            'project_name': request.form.get('project_name', ''),
        }

        # 如果未提供项目名称，自动生成
        if not config['project_name']:
            config['project_name'] = f"中国-{config['partner_country']}{config['major']}工匠学院"

        # 解析额外项目名称
        extra_project_names_str = request.form.get('extra_project_names', '[]')
        try:
            config['extra_project_names'] = json.loads(extra_project_names_str)
        except json.JSONDecodeError:
            config['extra_project_names'] = []

        # 解析选择的产品和自定义产品
        selected_items_str = request.form.get('selected_items', '[]')
        custom_items_str = request.form.get('custom_items', '[]')
        
        print(f"DEBUG /generate: selected_items_str = {selected_items_str[:100] if selected_items_str else 'None'}")
        print(f"DEBUG /generate: custom_items_str = {custom_items_str[:100] if custom_items_str else 'None'}")
        
        try:
            config['selected_items'] = json.loads(selected_items_str)
            config['custom_items'] = json.loads(custom_items_str)
            print(f"DEBUG /generate: selected_items count = {len(config['selected_items'])}")
            print(f"DEBUG /generate: custom_items count = {len(config['custom_items'])}")
        except json.JSONDecodeError as e:
            config['selected_items'] = []
            config['custom_items'] = []
            print(f"DEBUG /generate: JSON解析失败: {e}")

        # AI增强开关
        config['use_ai_enhancement'] = request.form.get('use_ai', 'true').lower() == 'true'

        # 解析第1章自定义内容
        section1_custom_items_str = request.form.get('section1_custom_items', '[]')
        try:
            config['section1_custom_items'] = json.loads(section1_custom_items_str)
        except json.JSONDecodeError:
            config['section1_custom_items'] = []

        # 解析第2章自定义内容
        section2_custom_items_str = request.form.get('section2_custom_items', '[]')
        try:
            config['section2_custom_items'] = json.loads(section2_custom_items_str)
        except json.JSONDecodeError:
            config['section2_custom_items'] = []

        # 解析第4章自定义内容
        section4_custom_items_str = request.form.get('section4_custom_items', '[]')
        try:
            config['section4_custom_items'] = json.loads(section4_custom_items_str)
        except json.JSONDecodeError:
            config['section4_custom_items'] = []

        # 解析第6章自定义内容
        section6_custom_items_str = request.form.get('section6_custom_items', '[]')
        try:
            config['section6_custom_items'] = json.loads(section6_custom_items_str)
        except json.JSONDecodeError:
            config['section6_custom_items'] = []

        # 解析第7章服务清单数据
        section7_service_list_str = request.form.get('section7_service_list', '[]')
        try:
            config['section7_service_list'] = json.loads(section7_service_list_str)
        except json.JSONDecodeError:
            config['section7_service_list'] = []

        # 解析第5章预期成果完成量数据
        section5_completion_data_str = request.form.get('section5_completion_data', '{}')
        try:
            config['section5_completion_data'] = json.loads(section5_completion_data_str)
        except json.JSONDecodeError:
            config['section5_completion_data'] = {}

        # 加载Excel产品数据
        parser = get_excel_parser()
        if parser:
            config['excel_products'] = parser.get_all_products_for_selection()

        # 生成方案
        generator = SolutionGenerator(config)
        generator.load_pricing_data()

        # 生成输出文件名
        school_short = config['school_name'][:8].replace(' ', '')
        output_filename = f"{school_short}_{config['major']}_建设方案.docx"
        output_path = os.path.join('output', output_filename)

        # 生成文档
        result_file = generator.generate(output_path)

        # 发送文件
        return send_file(
            result_file,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"生成失败: {str(e)}", 500


@app.route('/preview', methods=['POST'])
def preview():
    """预览方案内容"""
    try:
        config = {
            'school_name': request.form.get('school_name', DEFAULT_CONFIG['school_name']),
            'partner_country': request.form.get('partner_country', DEFAULT_CONFIG['partner_country']),
            'partner_institution': request.form.get('partner_institution', DEFAULT_CONFIG['partner_institution']),
            'chinese_enterprise': request.form.get('chinese_enterprise', DEFAULT_CONFIG.get('chinese_enterprise', '')),
            'major': request.form.get('major', DEFAULT_CONFIG['major']),
            'project_name': request.form.get('project_name', ''),
            'use_ai_enhancement': request.form.get('use_ai', 'false').lower() == 'true',  # AI增强开关
            'cover_image_url': request.form.get('cover_image_url', ''),  # 封面图片URL
        }

        if not config['project_name']:
            config['project_name'] = f"中国-{config['partner_country']}{config['major']}工匠学院"

        # 解析额外项目名称
        extra_project_names_str = request.form.get('extra_project_names', '[]')
        try:
            config['extra_project_names'] = json.loads(extra_project_names_str)
        except json.JSONDecodeError:
            config['extra_project_names'] = []

        # 解析选择的产品和自定义产品
        selected_items_str = request.form.get('selected_items', '[]')
        custom_items_str = request.form.get('custom_items', '[]')
        
        try:
            config['selected_items'] = json.loads(selected_items_str)
            config['custom_items'] = json.loads(custom_items_str)
        except json.JSONDecodeError:
            config['selected_items'] = []
            config['custom_items'] = []

        # 解析第1章自定义内容
        section1_custom_items_str = request.form.get('section1_custom_items', '[]')
        try:
            config['section1_custom_items'] = json.loads(section1_custom_items_str)
        except json.JSONDecodeError:
            config['section1_custom_items'] = []

        # 解析第2章自定义内容
        section2_custom_items_str = request.form.get('section2_custom_items', '[]')
        try:
            config['section2_custom_items'] = json.loads(section2_custom_items_str)
        except json.JSONDecodeError:
            config['section2_custom_items'] = []

        # 解析第4章自定义内容
        section4_custom_items_str = request.form.get('section4_custom_items', '[]')
        try:
            config['section4_custom_items'] = json.loads(section4_custom_items_str)
        except json.JSONDecodeError:
            config['section4_custom_items'] = []

        # 解析第6章自定义内容
        section6_custom_items_str = request.form.get('section6_custom_items', '[]')
        try:
            config['section6_custom_items'] = json.loads(section6_custom_items_str)
        except json.JSONDecodeError:
            config['section6_custom_items'] = []

        from generators.content_builder import ContentBuilder
        builder = ContentBuilder(config)
        sections = builder.build_all_sections()

        return render_template('preview.html', sections=sections, config=config)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"预览失败: {str(e)}", 500


@app.route('/api/upload-cover-image', methods=['POST'])
def upload_cover_image():
    """API: 上传封面图片"""
    try:
        if 'cover_image' not in request.files:
            return jsonify({'success': False, 'error': '没有上传图片'}), 400
        
        file = request.files['cover_image']
        if file.filename == '':
            return jsonify({'success': False, 'error': '文件名为空'}), 400
        
        # 检查文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'success': False, 'error': '不支持的文件格式，请上传PNG、JPG、GIF等图片格式'}), 400
        
        # 生成唯一文件名
        import uuid
        filename = f"cover_{uuid.uuid4().hex}.{file.filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(app.config['COVER_IMAGES_FOLDER'], filename)
        
        # 保存文件
        file.save(filepath)
        
        # 返回图片URL
        image_url = f"/uploads/{filename}"
        
        return jsonify({
            'success': True,
            'image_url': image_url,
            'filename': filename
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    """提供上传文件的访问"""
    from flask import send_from_directory
    return send_from_directory(app.config['COVER_IMAGES_FOLDER'], filename)


@app.route('/api/generate-ai-content', methods=['POST'])
def generate_ai_content():
    """API: AI生成指定小节的内容"""
    try:
        import json
        data = request.get_json()
        
        subsection_id = data.get('subsection_id', '')
        custom_title = data.get('custom_title', '')  # 自定义标题
        school_name = data.get('school_name', '')
        partner_country = data.get('partner_country', '')
        major = data.get('major', '')
        chinese_enterprise = data.get('chinese_enterprise', '')
        
        # 构建配置
        config = {
            'school_name': school_name,
            'partner_country': partner_country,
            'major': major,
            'chinese_enterprise': chinese_enterprise,
            'use_ai_enhancement': True
        }
        
        # 导入AI内容生成器
        from generators.ai_content_generator import AIContentGenerator
        
        ai_generator = AIContentGenerator()
        
        # 根据subsection_id或custom_title生成对应内容
        content_map = {
            'necessity_industry': lambda: ai_generator.enhance_necessity_analysis(config),
            'necessity_talent': lambda: ai_generator.generate_feasibility_analysis(config),
            'feasibility_policy': lambda: ai_generator.generate_feasibility_analysis(config),
            'feasibility_resource': lambda: ai_generator.generate_feasibility_analysis(config),
        }
        
        generator_func = content_map.get(subsection_id)
        if generator_func:
            generated_content = generator_func()
            return jsonify({
                'success': True,
                'content': generated_content,
                'subsection_id': subsection_id
            })
        else:
            # 处理自定义标题的情况
            if custom_title:
                # 根据标题关键词判断应该生成什么类型的内容
                if '必要' in custom_title or 'necessity' in custom_title.lower():
                    content = ai_generator.enhance_necessity_analysis(config)
                elif '可行' in custom_title or 'feasibility' in custom_title.lower():
                    content = ai_generator.generate_feasibility_analysis(config)
                else:
                    # 通用内容生成
                    content = f"【{custom_title}】\n\n基于{partner_country}{major}领域的产业发展需求，结合{school_name}的办学优势，本项目具有重要的战略意义和现实价值。\n\n一、产业背景\n当前，全球{major}产业正处于快速发展阶段，{partner_country}作为新兴经济体，对该领域人才需求旺盛。随着中国-{partner_country}产业合作的深入发展，双方在关键矿产、新能源材料、智能制造等领域的合作项目不断增加。\n\n二、人才需求\n据不完全统计，{partner_country}{major}相关产业人才缺口约50万人，急需高素质技术技能人才。特别是既懂专业技术又具备跨文化交流能力的复合型人才更为紧缺。\n\n三、合作基础\n{school_name}在{major}专业领域拥有丰富的教学经验和优质的教育资源，与{chinese_enterprise or '多家知名企业'}保持长期合作关系。通过引入国际标准和本土化改造，可实现专业优势的跨国输出。"
            else:
                # 默认生成通用内容
                if 'necessity' in subsection_id:
                    content = ai_generator.enhance_necessity_analysis(config)
                elif 'feasibility' in subsection_id:
                    content = ai_generator.generate_feasibility_analysis(config)
                else:
                    content = f"【{subsection_id}】\n\n基于{partner_country}{major}领域的产业发展需求，结合{school_name}的办学优势，本项目具有重要的战略意义和现实价值。\n\n一、产业背景\n当前，全球{major}产业正处于快速发展阶段，{partner_country}作为新兴经济体，对该领域人才需求旺盛。\n\n二、人才需求\n据不完全统计，{partner_country}{major}相关产业人才缺口约50万人，急需高素质技术技能人才。\n\n三、合作基础\n{school_name}在{major}专业领域拥有丰富的教学经验和优质的教育资源，与{chinese_enterprise or '多家知名企业'}保持长期合作关系。"
            
            return jsonify({
                'success': True,
                'content': content,
                'subsection_id': subsection_id
            })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("方案生成器 Web服务启动")
    print("="*60)
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
