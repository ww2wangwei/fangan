"""分析模板文档结构"""
import zipfile
import xml.etree.ElementTree as ET

# 读取document.xml
with zipfile.ZipFile('漳州职业第二轮双高建设内容实施方案.docx', 'r') as z:
    doc_xml = z.read('word/document.xml')
    styles_xml = z.read('word/styles.xml')
    
# 解析XML
root = ET.fromstring(doc_xml)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# 提取所有段落
paragraphs = root.findall('.//w:p', ns)
print(f"总段落数: {len(paragraphs)}")

print("\n=== 前30个段落详情 ===")
for i, p in enumerate(paragraphs[:30]):
    # 获取样式
    pPr = p.find('w:pPr', ns)
    style = 'None'
    if pPr is not None:
        pStyle = pPr.find('w:pStyle', ns)
        if pStyle is not None:
            style = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'None')
    
    # 获取文本
    texts = []
    for r in p.findall('.//w:t', ns):
        if r.text:
            texts.append(r.text)
    text = ''.join(texts).strip()
    
    if text or style != 'None':
        print(f"[{i:2d}] 样式:{style:20s} 文本:{text[:100]}")

# 提取表格
tables = root.findall('.//w:tbl', ns)
print(f"\n总表格数: {len(tables)}")

for i, tbl in enumerate(tables[:3]):
    print(f"\n=== 表格 {i+1} ===")
    rows = tbl.findall('.//w:tr', ns)
    print(f"行数: {len(rows)}")
    for j, row in enumerate(rows[:2]):
        cells = row.findall('.//w:tc', ns)
        cell_texts = []
        for cell in cells:
            texts = []
            for t in cell.findall('.//w:t', ns):
                if t.text:
                    texts.append(t.text)
            cell_texts.append(''.join(texts).strip())
        print(f"  行{j}: {' | '.join(cell_texts[:5])}")
