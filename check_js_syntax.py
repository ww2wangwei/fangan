#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check JavaScript syntax in index.html"""

with open('f:/方案生成器/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取<script>标签内容
script_start = content.find('<script>')
script_end = content.find('</script>') + 9
script_content = content[script_start:script_end]

print("Checking JavaScript syntax in <script> tag...\n")

# 逐字符分析字符串状态
in_double_string = False
in_single_string = False  
escape_next = False
line_num = 1
problems = []

for i, char in enumerate(script_content):
    if char == '\n':
        line_num += 1
    
    if escape_next:
        escape_next = False
        continue
        
    if char == '\\':
        escape_next = True
        continue
    
    # 处理双引号字符串
    if char == '"' and not in_single_string:
        in_double_string = not in_double_string
    
    # 处理单引号字符串  
    elif char == "'" and not in_double_string:
        in_single_string = not in_single_string
    
    # 记录问题位置（在字符串中遇到换行）
    if char == '\n' and (in_double_string or in_single_string):
        str_type = 'double' if in_double_string else 'single'
        problems.append((line_num, str_type))

if problems:
    print(f"[ERROR] Found {len(problems)} unclosed strings:")
    for line, str_type in problems[:5]:
        print(f"  Line {line}: Unclosed {str_type}-quoted string")
else:
    print("[OK] No unclosed strings found in JavaScript")

# 检查括号平衡
print("\nChecking bracket balance:")
parens = script_content.count('(') - script_content.count(')')
braces = script_content.count('{') - script_content.count('}')
brackets = script_content.count('[') - script_content.count(']')

print(f"  Parentheses (): {parens} ({'OK' if parens == 0 else 'MISMATCH'})")
print(f"  Braces {{}}: {braces} ({'OK' if braces == 0 else 'MISMATCH'})")
print(f"  Brackets []: {brackets} ({'OK' if brackets == 0 else 'MISMATCH'})")

if parens != 0 or braces != 0 or brackets != 0:
    print("\n[ERROR] Bracket mismatch detected!")
else:
    print("\n[OK] All brackets are balanced")

# 总结
print("\n" + "="*60)
if not problems and parens == 0 and braces == 0 and brackets == 0:
    print("[SUCCESS] JavaScript syntax looks OK!")
else:
    print("[FAILED] JavaScript syntax errors detected!")
print("="*60)
