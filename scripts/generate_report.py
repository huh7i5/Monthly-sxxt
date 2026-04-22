#!/usr/bin/env python3
"""
月报生成辅助脚本
功能：
  1. 将 Markdown 月报添加元数据头
  2. 自动命名输出文件
  3. (可选) 调用 pandoc 转换为 DOCX
"""

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path


def extract_metadata(content: str) -> dict:
    """从月报 Markdown 中提取元数据"""
    metadata = {
        "year": datetime.now().year,
        "month": datetime.now().month,
        "student_name": "未填写",
        "date": datetime.now().strftime("%Y年%m月%d日"),
    }

    # 尝试从标题提取年月
    title_match = re.search(r"#\s*(\d{4})年(\d{1,2})月", content)
    if title_match:
        metadata["year"] = int(title_match.group(1))
        metadata["month"] = int(title_match.group(2))

    # 尝试提取姓名
    name_match = re.search(r"\*\*姓名\*\*[：:]\s*(.+)", content)
    if name_match:
        metadata["student_name"] = name_match.group(1).strip()

    return metadata


def generate_filename(metadata: dict, ext: str = "md") -> str:
    """生成标准化文件名"""
    name = metadata["student_name"].replace(" ", "_")
    return f"{metadata['year']}年{metadata['month']:02d}月_月报_{name}.{ext}"


def add_generation_footer(content: str) -> str:
    """添加生成信息页脚"""
    footer = f"\n\n---\n\n> 本报告由月报生成器辅助生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    return content + footer


def convert_to_docx(input_path: Path, output_path: Path, reference_doc: Path = None):
    """使用 pandoc 转换为 DOCX"""
    if not shutil.which("pandoc"):
        print("⚠️  pandoc 未安装，跳过 DOCX 转换")
        print("   安装方法: https://pandoc.org/installing.html")
        return False

    import subprocess

    cmd = ["pandoc", str(input_path), "-o", str(output_path)]
    if reference_doc and reference_doc.exists():
        cmd.extend(["--reference-doc", str(reference_doc)])

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ DOCX 已生成: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ DOCX 转换失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="研究生月报生成辅助工具")
    parser.add_argument("--input", "-i", required=True, help="输入的 Markdown 月报文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径 (可选，默认自动命名)")
    parser.add_argument("--docx", action="store_true", help="同时生成 DOCX 格式")
    parser.add_argument(
        "--reference-doc", help="DOCX 参考模板路径 (用于样式)"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 输入文件不存在: {input_path}")
        return

    content = input_path.read_text(encoding="utf-8")
    metadata = extract_metadata(content)

    # 添加页脚
    content = add_generation_footer(content)

    # 确定输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / generate_filename(metadata)

    # 写入 Markdown
    output_path.write_text(content, encoding="utf-8")
    print(f"✅ 月报已生成: {output_path}")
    print(f"   姓名: {metadata['student_name']}")
    print(f"   月份: {metadata['year']}年{metadata['month']}月")

    # 可选：生成 DOCX
    if args.docx:
        docx_path = output_path.with_suffix(".docx")
        ref_doc = Path(args.reference_doc) if args.reference_doc else None
        convert_to_docx(output_path, docx_path, ref_doc)


if __name__ == "__main__":
    main()
