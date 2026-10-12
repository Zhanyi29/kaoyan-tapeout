import os
import glob
import re
import json

from parse_all_errors import parse_error_file

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

all_questions = []

for f in files:
    res = parse_error_file(f)
    paper_name = res['paper_name']
    paper_id = res['paper_id']
    
    # Map table rows by question number if available
    row_map = {}
    for r in res['table_rows']:
        # cols: 题号, 题型, 分值, 考场得分, 失分, 考查模块, 错因类型
        # Extract question number digits
        num_m = re.search(r'\d+', r[0])
        if num_m:
            row_map[num_m.group(0)] = r

    for q_num in res['p1_dict']:
        p1_title, p1_body = res['p1_dict'][q_num]
        p2_title, p2_body = res['p2_dict'].get(q_num, ("", ""))
        
        row_info = row_map.get(q_num, None)
        
        all_questions.append({
            'paper_id': paper_id,
            'paper_name': paper_name,
            'q_num': q_num,
            'p1_title': p1_title,
            'p1_body': p1_body,
            'p2_title': p2_title,
            'p2_body': p2_body,
            'row_info': row_info
        })

print(f"Total structured questions: {len(all_questions)}")

# Let's inspect 2016 rows or any missing rows
missing_rows = [q for q in all_questions if not q['row_info']]
print(f"Questions without overview row: {len(missing_rows)}")
for q in missing_rows:
    print(f"  {q['paper_name']} 第 {q['q_num']} 题: title={q['p1_title']}")

