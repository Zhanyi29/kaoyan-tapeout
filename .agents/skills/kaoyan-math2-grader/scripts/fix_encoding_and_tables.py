import os
import re

src = '错题/考研数学二_阶段复习(一)_全卷错题系统重构与攻坚总汇.md'

with open(src, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
fixed_table_cells = 0

for i, line in enumerate(lines):
    line_str = line
    # If this is a table row (starts and ends with |)
    if line_str.strip().startswith('|') and line_str.strip().endswith('|') and '---' not in line_str:
        # Check inside LaTeX $...$ or $$...$$ for unescaped |
        # Replace | inside $...$ with \|
        def replace_pipe_in_math(match):
            math_content = match.group(0)
            # replace unescaped | with \|
            # avoid already escaped \|
            fixed = re.sub(r'(?<!\\)\|', r'\\|', math_content)
            return fixed
        
        fixed_line = re.sub(r'\$.*?\$', replace_pipe_in_math, line_str)
        if fixed_line != line_str:
            fixed_table_cells += 1
            line_str = fixed_line
            
    # Also replace 4-byte emojis that might cause issues in some Windows viewers
    line_str = line_str.replace('💡', '[提示]').replace('🎯', '[重点]').replace('🌟', '[关键]')
    
    new_lines.append(line_str)

print(f"Fixed math pipe conflicts in tables: {fixed_table_cells}")

# Write back with utf-8-sig (UTF-8 with BOM)
with open(src, 'w', encoding='utf-8-sig') as f:
    f.writelines(new_lines)

print(f"Saved {src} with UTF-8 BOM (utf-8-sig) successfully.")
