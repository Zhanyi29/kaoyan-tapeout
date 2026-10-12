import os
import glob
import re

files = sorted(glob.glob('错题/*.md'))
print(f"Total error files: {len(files)}")

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    
    filename = os.path.basename(f)
    print(f"\n==========================================")
    print(f"FILE: {filename}")
    
    # print the first 40 lines to see header structure
    header = "".join(lines[:45])
    print(header)
