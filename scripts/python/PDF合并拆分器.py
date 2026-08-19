# 你是python专家，给我写个 PDF 合并/拆分器, 把多个 PDF 按指定顺序合并为一个，或提取指定页/范围保存为新文件，搭配 PyPDF2 或 pypdf。


# 下面是基于 `pypdf` 的 PDF 合并/拆分工具，支持命令行使用，包含页范围解析（如 `1-3,5,8-`）。

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 合并/拆分工具（基于 pypdf）
用法：
  python pdf_tool.py merge -o out.pdf in1.pdf in2.pdf ...
  python pdf_tool.py split -o out.pdf -p 1-3,5,8- in.pdf
"""
import argparse
import re
from pypdf import PdfReader, PdfWriter

# ---------- 合并 ----------
def merge_pdfs(pdf_list, output):
    writer = PdfWriter()
    for path in pdf_list:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output, "wb") as f:
        writer.write(f)
    print(f"合并完成：{output}（共 {len(writer.pages)} 页）")

# ---------- 页范围解析 ----------
def parse_pages(spec, total_pages):
    """解析 '1-3,5,8-' 为页码列表（从 1 开始）"""
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(\d*)-(\d*)$", part)
        if m:
            start = int(m.group(1)) if m.group(1) else 1
            end = int(m.group(2)) if m.group(2) else total_pages
            if start < 1 or end > total_pages or start > end:
                raise ValueError(f"无效范围: {part}")
            pages.extend(range(start, end + 1))
        else:
            p = int(part)
            if p < 1 or p > total_pages:
                raise ValueError(f"页码越界: {p}")
            pages.append(p)
    return [p - 1 for p in pages]  # 转为 0-based

# ---------- 拆分/提取 ----------
def split_pdf(input_pdf, output, page_spec):
    reader = PdfReader(input_pdf)
    total = len(reader.pages)
    pages = parse_pages(page_spec, total)

    writer = PdfWriter()
    for idx in pages:
        writer.add_page(reader.pages[idx])

    with open(output, "wb") as f:
        writer.write(f)
    print(f"提取完成：{output}（{len(pages)} / {total} 页）")

# ---------- 命令行入口 ----------
def main():
    parser = argparse.ArgumentParser(description="PDF 合并/拆分工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # merge 子命令
    mp = subparsers.add_parser("merge", help="合并多个 PDF")
    mp.add_argument("-o", "--output", required=True, help="输出文件")
    mp.add_argument("pdfs", nargs="+", help="按顺序输入的 PDF 文件列表")

    # split 子命令
    sp = subparsers.add_parser("split", help="提取指定页/范围")
    sp.add_argument("-o", "--output", required=True, help="输出文件")
    sp.add_argument("-p", "--pages", required=True,
                    help="页范围，如 '1-3,5,8-'")
    sp.add_argument("input_pdf", help="输入 PDF 文件")

    args = parser.parse_args()

    if args.command == "merge":
        merge_pdfs(args.pdfs, args.output)
    elif args.command == "split":
        split_pdf(args.input_pdf, args.output, args.pages)

if __name__ == "__main__":
    main()

## 使用说明

# 安装依赖
# pip install pypdf

# 合并：按传入顺序合并 1.pdf、2.pdf、3.pdf
# python pdf_tool.py merge -o merged.pdf 1.pdf 2.pdf 3.pdf

# 拆分：提取第 1、2、3、5、8 页及之后的所有页
# python pdf_tool.py split -o extracted.pdf -p "1-3,5,8-" input.pdf

# **页范围语法**：
# - `1-3` → 第 1 至 3 页
# - `5` → 第 5 页
# - `8-` → 第 8 页到末尾
# - `-3` → 第 1 页到第 3 页
# - 逗号组合 `1-3,5,8-`

# pypdf 是 PyPDF2 的现代继承者，API 相同但维护更活跃。若必须用 PyPDF2，只需 `pip install PyPDF2` 并 `from PyPDF2 import PdfReader, PdfWriter` 即可，其余代码不变。
