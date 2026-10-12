import os
import glob
import re
import json

files = [
    '错题/真题/2016年考研数学二真题_2026-09-17.md',
    '错题/真题/2017年考研数学二真题_2026-09-17.md',
    '错题/真题/2018年考研数学二真题_2026-09-18.md',
    '错题/真题/2019年考研数学二真题_2026-09-19.md',
    '错题/真题/2020年考研数学二真题_2026-09-20.md',
    '错题/真题/2021年考研数学二真题_2026-09-20.md',
    '错题/真题/2022年考研数学二真题_2026-09-22.md',
    '错题/真题/2023年考研数学二真题_2026-09-23.md',
    '错题/模拟卷/张宇/27张八/2027张宇八套卷_卷一_2026-09-20.md',
    '错题/模拟卷/张宇/27张八/2027张宇八套卷_卷二_2026-09-21.md',
    '错题/模拟卷/张宇/27张八/2027张宇八套卷_卷三_2026-09-24.md',
]

def parse_error_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Determine paper tag
    if '2016' in filename:
        paper_id = '2016'
        paper_name = '2016年真题'
    elif '2017' in filename:
        paper_id = '2017'
        paper_name = '2017年真题'
    elif '2018' in filename:
        paper_id = '2018'
        paper_name = '2018年真题'
    elif '2019' in filename:
        paper_id = '2019'
        paper_name = '2019年真题'
    elif '2020' in filename:
        paper_id = '2020'
        paper_name = '2020年真题'
    elif '2021' in filename:
        paper_id = '2021'
        paper_name = '2021年真题'
    elif '2022' in filename:
        paper_id = '2022'
        paper_name = '2022年真题'
    elif '2023' in filename:
        paper_id = '2023'
        paper_name = '2023年真题'
    elif '卷一' in filename:
        paper_id = 'ZY-1'
        paper_name = '2027张宇八套卷(一)'
    elif '卷二' in filename:
        paper_id = 'ZY-2'
        paper_name = '2027张宇八套卷(二)'
    elif '卷三' in filename:
        paper_id = 'ZY-3'
        paper_name = '2027张宇八套卷(三)'
    else:
        paper_id = 'OTHER'
        paper_name = filename

    # Split into Part 1 and Part 2 using regex line anchors
    p1_m = re.search(r'^#+\s*第一部分[^\n]*$', text, re.MULTILINE)
    p2_m = re.search(r'^#+\s*第二部分[^\n]*$', text, re.MULTILINE)
    p3_m = re.search(r'^#+\s*第三部分[^\n]*$', text, re.MULTILINE)

    if p1_m and p2_m:
        part1 = text[p1_m.end():p2_m.start()]
        part2 = text[p2_m.end():p3_m.start()] if p3_m else text[p2_m.end():]
    else:
        part1 = ""
        part2 = ""

    # Parse questions from Part 1 & Part 2
    # Question titles can be "### 第 3 题..." or "### 【第 3 题】..."
    q_pattern = r'(^###\s*【?第\s*(\d+)\s*题】?[^\n]*\n)(.*?)(?=(?:^###\s*【?第\s*\d+\s*题】?|\Z))'
    p1_items = re.findall(q_pattern, part1, re.DOTALL | re.MULTILINE)
    p2_items = re.findall(q_pattern, part2, re.DOTALL | re.MULTILINE)

    p1_dict = {m[1]: (m[0].strip(), m[2].strip().rstrip('-').strip()) for m in p1_items}
    p2_dict = {m[1]: (m[0].strip(), m[2].strip().rstrip('-').strip()) for m in p2_items}

    # Extract overview table rows
    table_rows = []
    lines = text.split('\n')
    in_tab = False
    for line in lines:
        if '## 错题概览与失分统计' in line:
            in_tab = True
            continue
        if in_tab:
            if line.startswith('|') and ('第' in line or '题' in line) and not '题号' in line and not '---' in line and not '合计' in line and not '总评' in line:
                cols = [c.strip() for c in line.split('|')[1:-1]]
                table_rows.append(cols)
            elif line.startswith('#') or (line.startswith('---') and len(table_rows) > 0):
                if len(table_rows) > 0:
                    break

    return {
        'paper_id': paper_id,
        'paper_name': paper_name,
        'filename': filename,
        'table_rows': table_rows,
        'p1_dict': p1_dict,
        'p2_dict': p2_dict
    }

all_results = []
for f in files:
    res = parse_error_file(f)
    all_results.append(res)
    print(f"Loaded {res['paper_name']}: {len(res['p1_dict'])} P1 questions, {len(res['p2_dict'])} P2 questions, {len(res['table_rows'])} table rows")

# Let's save a summary json for further inspection
print("Total papers parsed:", len(all_results))
