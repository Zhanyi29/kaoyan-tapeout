import glob
import os
import re

files = sorted(glob.glob('错题/*.md'))

summary = []

for f in files:
    fname = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # Check parts
    parts = re.split(r'#+\s*(?:第一部分|第二部分|第三部分)', content)
    
    # Try finding overview table rows
    table_rows = []
    lines = content.split('\n')
    for line in lines:
        line_s = line.strip()
        if line_s.startswith('|') and ('第' in line_s or '题' in line_s) and not '题号' in line_s and not '---' in line_s and not '合计' in line_s:
            cols = [c.strip() for c in line_s.split('|')[1:-1]]
            if len(cols) >= 6:
                table_rows.append(cols)
    
    summary.append({
        'file': fname,
        'table_rows': table_rows,
        'size': len(content),
        'has_part1': '第一部分' in content,
        'has_part2': '第二部分' in content,
        'has_part3': '第三部分' in content
    })

print(f"Total files: {len(summary)}")
for s in summary:
    print(f"\n[{s['file']}] (table rows: {len(s['table_rows'])})")
    for r in s['table_rows']:
        print("  |  ".join(r))
