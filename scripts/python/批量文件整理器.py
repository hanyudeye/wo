 # 给我做个**批量文件整理器** 自动按扩展名/日期/关键词把散乱的文件归类到文件夹，比如 `downloads/` 里的图片、PDF、压缩包一键归档，然后生成一些凌乱的测试文件让我测试下。


#!/usr/bin/env python3
"""批量文件整理器: 按扩展名/日期/关键词归类文件。"""

import argparse
import datetime
import random
import shutil
import string
import sys
from pathlib import Path

EXT_CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".ppt", ".pptx", ".epub"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tar.gz", ".tgz"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"},
    "video": {".mp4", ".avi", ".mkv", ".mov", ".flv", ".webm"},
    "code": {".py", ".js", ".ts", ".html", ".css", ".c", ".cpp", ".h", ".java", ".go", ".rs", ".sh", ".json", ".yaml", ".yml"},
    "executables": {".exe", ".msi", ".app", ".bin"},
}


def unique_dest(dest_dir: Path, name: str) -> Path:
    """重名时自动添加 (1), (2)..."""
    dest = dest_dir / name
    if not dest.exists():
        return dest
    stem, suffix = Path(name).stem, Path(name).suffix
    i = 1
    while True:
        dest = dest_dir / f"{stem} ({i}){suffix}"
        if not dest.exists():
            return dest
        i += 1


def category_for_file(path: Path) -> str:
    suffixes = [s.lower() for s in path.suffixes]
    if not suffixes:
        return "others"
    ext = suffixes[-1]
    if len(suffixes) >= 2 and suffixes[-2] == ".tar" and suffixes[-1] == ".gz":
        ext = ".tar.gz"
    for cat, exts in EXT_CATEGORIES.items():
        if ext in exts:
            return cat
    return "others"


def organize_by_ext(source: Path):
    for item in sorted(source.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        if item.name == Path(__file__).name:
            continue
        category = category_for_file(item)
        dest_dir = source / category
        dest_dir.mkdir(exist_ok=True)
        dest = unique_dest(dest_dir, item.name)
        shutil.move(str(item), str(dest))
        print(f"  {item.name} -> {dest.relative_to(source)}")


def organize_by_date(source: Path):
    for item in sorted(source.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        if item.name == Path(__file__).name:
            continue
        mtime = datetime.datetime.fromtimestamp(item.stat().st_mtime)
        dest_dir = source / str(mtime.year) / f"{mtime.month:02d}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = unique_dest(dest_dir, item.name)
        shutil.move(str(item), str(dest))
        print(f"  {item.name} -> {dest.relative_to(source)}")


def organize_by_keyword(source: Path, keywords: list):
    for item in sorted(source.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        if item.name == Path(__file__).name:
            continue
        lowered = item.name.lower()
        matched = next((kw for kw in keywords if kw.lower() in lowered), None)
        dest_dir = source / (matched if matched else "misc")
        dest_dir.mkdir(exist_ok=True)
        dest = unique_dest(dest_dir, item.name)
        shutil.move(str(item), str(dest))
        print(f"  {item.name} -> {dest.relative_to(source)}")


def random_string(n: int) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def make_test_files(target: Path, count: int = 60, seed: int = 42):
    """生成散乱测试文件。"""
    target.mkdir(parents=True, exist_ok=True)
    extensions = [".jpg", ".png", ".gif", ".pdf", ".docx", ".txt",
                  ".zip", ".tar.gz", ".mp3", ".mp4", ".py", ".js", ".xlsx"]
    keywords = ["report", "travel", "photo", "backup", "meeting", "music", "invoice"]
    random.seed(seed)
    for i in range(count):
        ext = random.choice(extensions)
        if random.random() < 0.7:
            kw = random.choice(keywords)
            name = f"{kw}_{random_string(4)}{ext}"
        else:
            name = f"file_{i}_{random_string(3)}{ext}"
        (target / name).write_text("dummy content", encoding="utf-8")

    (target / "subfolder").mkdir(exist_ok=True)
    (target / "subfolder" / "note.txt").write_text("hello", encoding="utf-8")
    print(f"已生成 {count} 个散乱测试文件到: {target}")


def main():
    parser = argparse.ArgumentParser(description="批量文件整理器")
    sub = parser.add_subparsers(dest="command", required=True)

    org = sub.add_parser("organize", help="整理文件")
    org.add_argument("--dir", type=Path, default=Path.home() / "Downloads", help="要整理的目录")
    org.add_argument("--method", choices=["ext", "date", "keyword"], default="ext", help="整理方式")
    org.add_argument("--keywords", nargs="+", default=[], help="关键字（method=keyword 时使用）")

    test = sub.add_parser("make-test", help="生成凌乱测试文件")
    test.add_argument("--dir", type=Path, default=Path("test_downloads"), help="生成到哪个目录")
    test.add_argument("--count", type=int, default=60)
    test.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if args.command == "make-test":
        make_test_files(args.dir, args.count, args.seed)
    elif args.command == "organize":
        if not args.dir.is_dir():
            sys.exit(f"目录不存在: {args.dir}")
        print(f"整理 {args.dir} ...")
        if args.method == "ext":
            organize_by_ext(args.dir)
        elif args.method == "date":
            organize_by_date(args.dir)
        elif args.method == "keyword":
            if not args.keywords:
                sys.exit("请提供 --keywords 参数，例如: --keywords report travel photo")
            organize_by_keyword(args.dir, args.keywords)
        print("完成。")


if __name__ == "__main__":
    main()

## 用法

# # 1. 生成 60 个散乱测试文件到 ./test_downloads
# python organizer.py make-test --dir ./test_downloads

# # 2. 按扩展名整理
# python organizer.py organize --dir ./test_downloads --method ext

# # 按日期整理（年/月子目录）
# python organizer.py organize --dir ./test_downloads --method date

# # 按关键字整理
# python organizer.py organize --dir ./test_downloads --method keyword --keywords report travel photo

# # 运行后，图片、PDF、压缩包等会自动归入对应的 `images/`、`documents/`、`archives/` 等文件夹。
