import asyncio
import os
import sys
import json
import time
import pymupdf
from playwright.async_api import async_playwright

assets_dir = os.path.abspath('tools/assets').replace('\\', '/')

def create_html_for_markdown(md_text, title, is_pure_question=False):
    # CSS styling tailored for exam papers and study documents
    css = f"""
    @page {{
        size: A4;
        margin: 18mm 15mm 18mm 15mm;
        @bottom-right {{
            content: counter(page) " / " counter(pages);
            font-size: 9pt;
            color: #718096;
            font-family: -apple-system, 'Microsoft YaHei', sans-serif;
        }}
        @top-left {{
            content: "{title}";
            font-size: 8.5pt;
            color: #a0aec0;
            font-family: -apple-system, 'Microsoft YaHei', sans-serif;
            border-bottom: 0.5px solid #e2e8f0;
            padding-bottom: 2mm;
        }}
    }}
    *, *::before, *::after {{
        box-sizing: border-box;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
        font-size: 10pt;
        line-height: 1.65;
        color: #2d3748;
        background: #ffffff;
        margin: 0;
        padding: 0;
    }}
    h1 {{
        font-size: 18pt;
        font-weight: 700;
        color: #1a365d;
        text-align: center;
        margin-top: 0;
        margin-bottom: 12pt;
        padding-bottom: 8pt;
        border-bottom: 2px solid #2b6cb0;
        page-break-after: avoid;
    }}
    h2 {{
        font-size: 13pt;
        font-weight: 600;
        color: #2b6cb0;
        margin-top: 18pt;
        margin-bottom: 8pt;
        padding: 4pt 8pt;
        background: #ebf8ff;
        border-left: 4px solid #3182ce;
        border-radius: 2px;
        page-break-after: avoid;
        page-break-inside: avoid;
    }}
    h3 {{
        font-size: 11pt;
        font-weight: 600;
        color: #2d3748;
        margin-top: 14pt;
        margin-bottom: 6pt;
        padding-bottom: 2pt;
        border-bottom: 1px dashed #cbd5e0;
        page-break-after: avoid;
        page-break-inside: avoid;
    }}
    h4 {{
        font-size: 10pt;
        font-weight: 600;
        color: #4a5568;
        margin-top: 10pt;
        margin-bottom: 4pt;
        page-break-after: avoid;
    }}
    p {{
        margin-top: 4pt;
        margin-bottom: 6pt;
        text-align: justify;
    }}
    blockquote {{
        margin: 8pt 0;
        padding: 6pt 10pt;
        background: #f7fafc;
        border-left: 3.5px solid #4299e1;
        font-size: 9.5pt;
        color: #4a5568;
        border-radius: 2px;
        page-break-inside: avoid;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 10pt 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }}
    th, td {{
        border: 1px solid #cbd5e0;
        padding: 5pt 7pt;
        text-align: left;
        vertical-align: middle;
    }}
    th {{
        background-color: #edf2f7;
        font-weight: 600;
        color: #2d3748;
    }}
    tr:nth-child(even) td {{
        background-color: #f7fafc;
    }}
    hr {{
        border: 0;
        height: 1px;
        background: #e2e8f0;
        margin: 14pt 0;
    }}
    code {{
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
        background-color: #edf2f7;
        padding: 1pt 3pt;
        border-radius: 2px;
        color: #805ad5;
    }}
    pre {{
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 8pt 10pt;
        margin: 8pt 0;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
        line-height: 1.5;
        white-space: pre-wrap;
        word-wrap: break-word;
        page-break-inside: avoid;
    }}
    .katex {{
        font-size: 1.05em;
    }}
    .katex-display {{
        margin: 6pt 0;
        overflow-x: visible;
        page-break-inside: avoid;
    }}
    ul, ol {{
        margin: 4pt 0 6pt 16pt;
        padding: 0;
    }}
    li {{
        margin-bottom: 2pt;
    }}
    /* Print specific optimization */
    @media print {{
        body {{
            background: #ffffff;
        }}
    }}
    """

    json_md = json.dumps(md_text)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="{assets_dir}/katex.min.css">
<script src="{assets_dir}/marked.min.js"></script>
<script src="{assets_dir}/katex.min.js"></script>
<script src="{assets_dir}/auto-render.min.js"></script>
<style>
{css}
</style>
</head>
<body>
<div id="content"></div>
<script>
window.rendered = false;
try {{
    const rawMd = {json_md};
    // Configure marked options
    marked.setOptions({{
        gfm: true,
        breaks: true
    }});
    document.getElementById('content').innerHTML = marked.parse(rawMd);
    
    // Render math with KaTeX
    renderMathInElement(document.getElementById('content'), {{
        delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$', right: '$', display: false}},
            {{left: '\\\\(', right: '\\\\)', display: false}},
            {{left: '\\\\[', right: '\\\\]', display: true}}
        ],
        throwOnError: false
    }});
    window.rendered = true;
}} catch(e) {{
    console.error(e);
    window.rendered = 'error: ' + e.message;
}}
</script>
</body>
</html>"""
    return html

async def convert_file(md_path, pdf_path, title, is_pure_question=False):
    print(f"\n==========================================")
    print(f"Converting: {os.path.basename(md_path)}")
    print(f"Target PDF: {os.path.basename(pdf_path)}")
    
    with open(md_path, 'r', encoding='utf-8-sig') as f:
        md_text = f.read()

    html_content = create_html_for_markdown(md_text, title, is_pure_question)
    temp_html_path = md_path.replace('.md', '_temp.html')
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    t0 = time.time()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        file_url = 'file:///' + os.path.abspath(temp_html_path).replace('\\', '/')
        await page.goto(file_url, wait_until='networkidle')
        await page.wait_for_function('window.rendered === true || typeof window.rendered === "string"')
        status = await page.evaluate('window.rendered')
        if status != True:
            print("Render status error:", status)
            
        # Give KaTeX a tiny fraction to finalize layout
        await page.wait_for_timeout(800)
        
        # Output PDF with custom margins and background
        await page.pdf(
            path=pdf_path,
            format='A4',
            print_background=True,
            margin={
                'top': '18mm',
                'bottom': '18mm',
                'left': '15mm',
                'right': '15mm'
            },
            display_header_footer=True,
            header_template=f'''
                <div style="font-size: 8pt; color: #a0aec0; width: 100%; text-align: left; margin-left: 15mm; margin-right: 15mm; border-bottom: 0.5px solid #edf2f7; padding-bottom: 2px; font-family: -apple-system, sans-serif;">
                    <span>{title}</span>
                </div>
            ''',
            footer_template='''
                <div style="font-size: 8pt; color: #718096; width: 100%; text-align: right; margin-right: 15mm; font-family: -apple-system, sans-serif;">
                    <span class="pageNumber"></span> / <span class="totalPages"></span>
                </div>
            '''
        )
        await browser.close()

    elapsed = round(time.time() - t0, 2)
    # Remove temp html
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    # Validate output PDF with PyMuPDF
    doc = pymupdf.open(pdf_path)
    page_count = len(doc)
    file_size_kb = round(os.path.getsize(pdf_path) / 1024, 1)
    print(f"Generated successfully in {elapsed}s!")
    print(f"PDF Pages: {page_count}, File Size: {file_size_kb} KB")
    return page_count, file_size_kb

async def main():
    tasks = [
        (
            '错题/考研数学二_阶段复习(一)_79题纯题目重做卷(无答案版).md',
            '错题/考研数学二_阶段复习(一)_79题纯题目重做卷(无答案版).pdf',
            '考研数学二 · 阶段复习（一）79题纯题目重做卷（闭卷自测版）',
            True
        ),
        (
            '错题/考研数学二_阶段复习(一)_全卷错题系统重构与攻坚总汇.md',
            '错题/考研数学二_阶段复习(一)_全卷错题系统重构与攻坚总汇.pdf',
            '考研数学二 · 阶段复习（一）全卷错题系统重构与攻坚总汇（一题一解精研版）',
            False
        )
    ]
    
    for md_p, pdf_p, title, is_pure in tasks:
        await convert_file(md_p, pdf_p, title, is_pure)

if __name__ == '__main__':
    asyncio.run(main())
