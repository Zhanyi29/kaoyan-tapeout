import os
import sys
import re

sys.path.append('scratch')
from verify_mapping import topic_map, topic_names
from structure_questions import all_questions

# Organize questions by topic
topics_data = {tid: [] for tid in range(1, 13)}

# Extract manual info for 2016 if needed
manual_2016 = {
    '3': {'type': '单项选择题', 'score': 4, 'name': '反常积分审敛判别'},
    '12': {'type': '填空题', 'score': 4, 'name': '变限积分方程与高阶导数'},
    '15': {'type': '解答题', 'score': 10, 'name': '1^inf 未定式极限'},
    '16': {'type': '解答题', 'score': 10, 'name': '变限绝对值定积分分段最值'},
    '18': {'type': '解答题', 'score': 10, 'name': '二重积分极坐标与三角积分'},
    '19': {'type': '解答题', 'score': 10, 'name': '二阶可降阶微分方程通解'},
    '21': {'type': '解答题', 'score': 11, 'name': '平均值与导数零点定理证明'}
}

for q in all_questions:
    p_id = q['paper_id']
    q_num = q['q_num']
    tid = topic_map.get((p_id, q_num), 1)
    topics_data[tid].append(q)

target_file = '错题/考研数学二_阶段复习(一)_79题纯题目重做卷(无答案版).md'

with open(target_file, 'w', encoding='utf-8-sig') as out:
    # Header
    out.write("# 考研数学二 · 阶段复习（一）79题纯题目重做卷（无答案闭卷自测版）\n\n")
    out.write("> **试卷性质**：阶段复习（一）专项闭卷训练卷（纯题目版）  \n")
    out.write("> **试卷范围**：全卷收录 2016～2023 年 8 套考研数学二真题 + 2027版张宇八套卷（卷一、卷二、卷三）共 11 套试卷的 **全部 79 道错题**  \n")
    out.write("> **总分规模**：共 79 题，总满分 **635分**（选择题 25 题 · 113分；填空题 14 题 · 69分；解答题 40 题 · 453分）  \n")
    out.write("> **排版规范**：本卷为 **100% 纯试题排版**，不含任何标准答案、解析步骤、得分记录或错因提示。每道选择题/填空题预留答案填写线，每道解答题预留答题推导区，可直接用于在平板（如 GoodNotes / Notability）闭卷书写、直接打印练习，或在本地 Markdown 编辑器中独立作答。  \n")
    out.write("> **核对答案**：全套题目的官方标准答案、严谨步骤分值拆解与考场错因深度诊断，请直接查阅：[考研数学二_阶段复习(一)_全卷错题系统重构与攻坚总汇.md](file:///f:/Projects/personal/批改/错题/考研数学二_阶段复习(一)_全卷错题系统重构与攻坚总汇.md)。\n\n")
    out.write("---\n\n")

    # Navigation & Topic Index
    out.write("## 12 大专题快速导航与题量索引\n\n")
    out.write("| 专题编号 | 专题知识模块 | 题量 | 涵盖题型 | 建议限时 | 完成进度 |\n")
    out.write("| :---: | :--- | :---: | :--- | :---: | :---: |\n")
    
    topic_times = {
        1: "45 分钟", 2: "35 分钟", 3: "90 分钟", 4: "70 分钟",
        5: "35 分钟", 6: "65 分钟", 7: "45 分钟", 8: "45 分钟",
        9: "50 分钟", 10: "45 分钟", 11: "30 分钟", 12: "50 分钟"
    }

    for tid in range(1, 13):
        tname = topic_names[tid]
        q_list = topics_data[tid]
        q_types = set()
        for q in q_list:
            t_orig = q['p1_title']
            if '选择' in t_orig:
                q_types.add('选择')
            elif '填空' in t_orig:
                q_types.add('填空')
            else:
                q_types.add('解答')
        types_str = "、".join(sorted(list(q_types)))
        out.write(f"| **专题 {tid}** | [{tname}](#{tname.lower().replace('：', '').replace('（', '').replace('）', '').replace('——', '').replace('、', '').replace(' ', '-')}) | **{len(q_list)} 题** | {types_str} | {topic_times[tid]} | [ ] 未开始 |\n")

    out.write("\n---\n---\n\n")

    # Output Questions Topic by Topic
    total_q_counter = 0

    for tid in range(1, 13):
        tname = topic_names[tid]
        q_list = topics_data[tid]
        out.write(f"## {tname}（共 {len(q_list)} 题）\n\n")
        out.write(f"> **专题目标**：检验该专题核心概念、典型解法模型与运算推导闭环。建议限时 **{topic_times[tid]}** 完成。\n\n")

        for idx, q in enumerate(q_list, 1):
            total_q_counter += 1
            p_name = q['paper_name']
            q_num = q['q_num']
            p_id = q['paper_id']
            
            # Determine question type and score
            if q['row_info']:
                row = q['row_info']
                q_type = row[1]
                q_score = row[2]
                q_topic_desc = row[5]
            elif p_id == '2016' and q_num in manual_2016:
                info = manual_2016[q_num]
                q_type = info['type']
                q_score = f"{info['score']}分"
                q_topic_desc = info['name']
            else:
                q_type = '填空题' if q_num == '14' else '解答题'
                q_score = '5分'
                q_topic_desc = '平面曲线曲率最值'

            # Clean original title
            # Title header format: ### 【题 X-Y】题型（满分 X分）｜ 来源：...
            out.write(f"### 【题 {tid}-{idx}】{q_type}（满分 {q_score}）｜ 来源：{p_name} 第 {q_num} 题\n\n")

            # Question Body
            body_clean = q['p1_body'].strip()
            # Ensure no double headers
            lines = body_clean.split('\n')
            if lines and lines[0].startswith('#'):
                body_clean = '\n'.join(lines[1:]).strip()

            out.write(f"{body_clean}\n\n")

            # Answer space according to question type
            if '选择' in q_type:
                out.write("**【你的答案】**：`[    ]`\n\n")
                out.write("**【速记草稿 / 排除理由】**：\n\n")
                out.write("```\n\n```\n\n")
            elif '填空' in q_type:
                out.write("**【你的填空结果】**：___________________________\n\n")
                out.write("**【核心计算步骤草稿】**：\n\n")
                out.write("```\n\n```\n\n")
            else:
                # Big question (解答题)
                out.write("**【你的规范解题过程与书写区】**：\n\n")
                out.write("```markdown\n【解】\n\n\n\n\n\n\n\n\n\n```\n\n")

            out.write("---\n\n")

        out.write("\n---\n\n")

    # Appendix: Check table
    out.write("# 附录：全卷 79 题二刷通关打卡自测表\n\n")
    out.write("> 💡 **使用方法**：完成对应题目的闭卷独立作答后，对照解析文档进行严格自评打分，并在对应行标注完成状态。\n\n")
    out.write("| 序号 | 专题编号 | 试卷与题号 | 题型 | 满分 | 二刷得分 | 掌握情况标记 | 核心失误点（如有） |\n")
    out.write("| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |\n")

    q_idx_counter = 0
    for tid in range(1, 13):
        q_list = topics_data[tid]
        for idx, q in enumerate(q_list, 1):
            q_idx_counter += 1
            p_name = q['paper_name']
            q_num = q['q_num']
            p_id = q['paper_id']
            if q['row_info']:
                row = q['row_info']
                q_type = row[1]
                q_score = row[2]
            elif p_id == '2016' and q_num in manual_2016:
                info = manual_2016[q_num]
                q_type = info['type']
                q_score = f"{info['score']}分"
            else:
                q_type = '填空题' if q_num == '14' else '解答题'
                q_score = '5分'
            out.write(f"| {q_idx_counter} | 题 {tid}-{idx} | {p_name} 第 {q_num} 题 | {q_type} | {q_score} | _____ 分 | [ ] 完全掌握  [ ] 仍有瑕疵 | |\n")

    out.write("\n---\n\n")
    out.write("> 🔗 **对照解析入口**：[考研数学二_阶段复习(一)_全卷错题系统重构与攻坚总汇.md](file:///f:/Projects/personal/批改/错题/考研数学二_阶段复习(一)_全卷错题系统重构与攻坚总汇.md)\n")

print(f"Pure question paper generated successfully: {target_file}")
