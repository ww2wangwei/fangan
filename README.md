# 职业教育国际化方案生成器

## 项目简介

这是一个面向职业教育国际化的智能方案生成工具,基于厚溥国际职业教育产品报价单和实际建设方案模板,帮助快速生成标准化的项目建设方案。

## 功能特性

- **智能解析**: 自动读取Excel报价单,提取产品和服务数据
- **模板驱动**: 基于真实建设方案模板,生成标准化文档
- **灵活配置**: 支持自定义学校名称、合作国家、专业方向等参数
- **一键生成**: 自动生成包含项目背景、建设目标、实施内容、预算报价的完整方案
- **多格式输出**: 支持Word(.docx)和PDF格式输出

## 使用方式

### 命令行模式

```bash
python main.py --school "广西现代职业技术学院" --country "印度" --major "工业机器人" --output "方案.docx"
```

### 交互模式

```bash
python main.py --interactive
```

## 项目结构

```
方案生成器/
├── main.py                 # 主程序入口
├── config/
│   └── settings.py        # 配置文件
├── parsers/
│   ├── excel_parser.py    # Excel报价单解析器
│   └── pdf_parser.py      # PDF模板解析器
├── generators/
│   ├── doc_generator.py   # Word文档生成器
│   └── content_builder.py # 内容构建器
├── templates/
│   └── sections/          # 方案章节模板
├── data/
│   └── cache.json         # 缓存数据
└── output/                # 生成的方案文件
```

## 依赖安装

```bash
pip install openpyxl python-docx PyPDF2 jinja2
```

## 核心模块说明

### 1. Excel解析器 (`parsers/excel_parser.py`)
解析厚溥国际产品报价单,提取:
- 国际化产品服务(院校对接、专业标准、课程标准等)
- 印度考察项目费用
- 视频资源成本
- 产品清单和备注信息

### 2. 内容构建器 (`generators/content_builder.py`)
根据输入参数动态生成方案内容:
- 项目背景与必要性分析
- 建设目标与规划
- 实施内容与时间表
- 预算报价明细
- 预期成果

### 3. 文档生成器 (`generators/doc_generator.py`)
使用python-docx生成格式化的Word文档,包含:
- 封面页
- 目录
- 正文各章节
- 表格(预算表、进度表等)

## 示例输出

生成的方案包含以下章节:
1. 项目建设的必要性和可行性
2. 项目建设规划
3. 建设内容
4. 协同推动职教出海
5. 预期成果
6. 项目预算
7. 项目保障

## License

内部工具,仅供授权使用。
