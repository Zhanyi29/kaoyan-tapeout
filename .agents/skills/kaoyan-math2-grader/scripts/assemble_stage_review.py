import os
import re
import json

from verify_mapping import topic_map, topic_names
from structure_questions import all_questions

# Organize questions by topic
topics_data = {tid: [] for tid in range(1, 13)}

# Assign sequential ID in stage review: e.g. T1-01, T1-02, ...
for q in all_questions:
    p_id = q['paper_id']
    q_num = q['q_num']
    tid = topic_map.get((p_id, q_num), 1)
    topics_data[tid].append(q)

print("Topics grouping finished. Checking counts:")
for tid in range(1, 13):
    print(f"Topic {tid}: {len(topics_data[tid])} questions")

