import glob
import os
import re

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

all_data = []

for f in files:
    fname = os.path.basename(f)
    paper_title = fname.replace('_错题集与官方解析.md', '').replace('.md', '')
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # Extract questions in part 1 (题目汇总篇)
    part1_match = re.search(r'#+\s*第一部分[^\n]*\n(.*?)(?=#+\s*第二部分|\Z)', content, re.DOTALL)
    part1_text = part1_match.group(1) if part1_match else ""
    
    part2_match = re.search(r'#+\s*第二部分[^\n]*\n(.*?)(?=#+\s*第三部分|\Z)', content, re.DOTALL)
    part2_text = part2_match.group(1) if part2_match else ""

    part3_match = re.search(r'#+\s*第三部分[^\n]*\n(.*)', content, re.DOTALL)
    part3_text = part3_match.group(1) if part3_match else ""

    # Let's find question blocks in part 1
    # Typically ### 【第 X 题】... or ### 第 X 题...
    q_blocks_p1 = re.findall(r'(###\s*【?第\s*(\d+)\s*题】?[^\n]*)\n(.*?)(?=\n###|\n---|\Z)', part1_text, re.DOTALL)
    
    # Also find question blocks in part 2
    q_blocks_p2 = re.findall(r'(###\s*【?第\s*(\d+)\s*题】?[^\n]*)\n(.*?)(?=\n###|\n---|\Z)', part2_text, re.DOTALL)

    print(f"=== {paper_title} ===")
    print(f"Part1 questions found: {len(q_blocks_p1)}, Part2 questions found: {len(q_blocks_p2)}")
    q_nums_p1 = [m[1] for m in q_blocks_p1]
    q_nums_p2 = [m[1] for m in q_blocks_p2]
    print(f"P1 Qs: {q_nums_p1}")
    print(f"P2 Qs: {q_nums_p2}")
