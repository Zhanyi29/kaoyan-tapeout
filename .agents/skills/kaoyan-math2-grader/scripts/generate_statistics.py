import os
import glob
import re
import json

from verify_mapping import topic_map, topic_names
from structure_questions import all_questions

paper_stats = {}
error_type_stats = {
    'A. 概念/性质理解不清/混淆': 0,
    'B. 方法选择不当/思维受阻': 0,
    'C. 综合转化能力欠缺/逻辑漏洞': 0,
    'D. 计算失误/代数变形笔误': 0,
    'E. 审题疏忽/漏读条件': 0,
    'F. 书写规范/跳步/格式瑕疵': 0
}

# For 2016 manual info:
manual_2016 = {
    '3': {'type': '单项选择题', 'score': 4, 'deduct': 4, 'module': '反常积分审敛判别', 'err': 'B. 方法选择不当/思维受阻'},
    '12': {'type': '填空题', 'score': 4, 'deduct': 4, 'module': '变限积分方程与高阶导数', 'err': 'D. 计算失误/代数变形笔误'},
    '15': {'type': '解答题', 'score': 10, 'deduct': 3, 'module': '1^inf 极限与泰勒展开', 'err': 'D. 计算失误/代数变形笔误'},
    '16': {'type': '解答题', 'score': 10, 'deduct': 2, 'module': '变限绝对值定积分分段求导最值', 'err': 'F. 书写规范/跳步/格式瑕疵'},
    '18': {'type': '解答题', 'score': 10, 'deduct': 5, 'module': '二重积分极坐标与三角积分', 'err': 'D. 计算失误/代数变形笔误'},
    '19': {'type': '解答题', 'score': 10, 'deduct': 6, 'module': '二阶可降阶微分方程通解', 'err': 'C. 综合转化能力欠缺/逻辑漏洞'},
    '21': {'type': '解答题', 'score': 11, 'deduct': 1, 'module': '平均值与导数零点定理证明', 'err': 'F. 书写规范/跳步/格式瑕疵'}
}

total_deduct_all = 0
total_score_all = 0
obj_deduct = 0
subj_deduct = 0

for q in all_questions:
    p_id = q['paper_id']
    p_name = q['paper_name']
    q_num = q['q_num']
    
    if p_name not in paper_stats:
        paper_stats[p_name] = {'count': 0, 'score': 0, 'deduct': 0, 'obj_deduct': 0, 'subj_deduct': 0}
    
    paper_stats[p_name]['count'] += 1
    
    # row info: 题号, 题型, 分值, 考场得分, 失分, 考查模块, 错因类型
    if q['row_info']:
        row = q['row_info']
        q_type = row[1]
        score_val = int(re.search(r'\d+', row[2]).group(0))
        # deduct
        deduct_val = int(re.search(r'\d+', row[4]).group(0))
        module_val = row[5]
        err_val = row[6]
    elif p_id == '2016' and q_num in manual_2016:
        info = manual_2016[q_num]
        q_type = info['type']
        score_val = info['score']
        deduct_val = info['deduct']
        module_val = info['module']
        err_val = info['err']
    else:
        q_type = '填空题' if q_num == '14' else '解答题'
        score_val = 5
        deduct_val = 5
        module_val = '平面曲线曲率公式与极值最值'
        err_val = 'D. 计算失误'
        
    paper_stats[p_name]['score'] += score_val
    paper_stats[p_name]['deduct'] += deduct_val
    total_deduct_all += deduct_val
    total_score_all += score_val
    
    if '选择' in q_type or '填空' in q_type:
        paper_stats[p_name]['obj_deduct'] += deduct_val
        obj_deduct += deduct_val
    else:
        paper_stats[p_name]['subj_deduct'] += deduct_val
        subj_deduct += deduct_val
        
    # classify error type
    err_str = err_val.upper()
    if 'A' in err_str or '概念' in err_str or '性质' in err_str:
        error_type_stats['A. 概念/性质理解不清/混淆'] += 1
    if 'B' in err_str or '方法' in err_str:
        error_type_stats['B. 方法选择不当/思维受阻'] += 1
    if 'C' in err_str or '转化' in err_str or '逻辑' in err_str:
        error_type_stats['C. 综合转化能力欠缺/逻辑漏洞'] += 1
    if 'D' in err_str or '计算' in err_str or '笔误' in err_str:
        error_type_stats['D. 计算失误/代数变形笔误'] += 1
    if 'E' in err_str or '审题' in err_str or '漏' in err_str:
        error_type_stats['E. 审题疏忽/漏读条件'] += 1
    if 'F' in err_str or '规范' in err_str or '书写' in err_str or '跳步' in err_str:
        error_type_stats['F. 书写规范/跳步/格式瑕疵'] += 1

print("=== 试卷统计表 ===")
print(f"{'试卷名称':<20} | 错题数 | 总分值 | 失分总计 | 客观题失分 | 主观题失分")
print("-" * 65)
for p_name, st in paper_stats.items():
    print(f"{p_name:<20} | {st['count']:^6} | {st['score']:^6} | {st['deduct']:^8} | {st['obj_deduct']:^10} | {st['subj_deduct']:^10}")
print("-" * 65)
print(f"总计: 11套试卷 | 错题数: {len(all_questions)} | 涉及满分: {total_score_all}分 | 失分: {total_deduct_all}分 (客观题: {obj_deduct}分, 主观题: {subj_deduct}分)")

print("\n=== 错因类型分布 (可能多重标记) ===")
for et, c in error_type_stats.items():
    print(f"{et}: {c} 次")
