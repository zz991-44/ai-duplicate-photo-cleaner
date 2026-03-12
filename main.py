#!/usr/bin/env python3
import os
import argparse
from PIL import Image
import imagehash
from tqdm import tqdm
from send2trash import send2trash
import json
from collections import defaultdict

SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

def get_image_hash(image_path, hash_size=16):
    """计算图片的感知哈希值"""
    try:
        with Image.open(image_path) as img:
            return str(imagehash.dhash(img, hash_size=hash_size))
    except Exception as e:
        print(f"无法处理图片 {image_path}: {e}")
        return None

def find_duplicates(directory, threshold=0, hash_size=16):
    """查找目录下的重复图片"""
    hashes = defaultdict(list)
    image_files = []
    
    # 遍历目录收集所有图片
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(SUPPORTED_FORMATS):
                image_files.append(os.path.join(root, file))
    
    print(f"共找到 {len(image_files)} 张图片，正在计算哈希值...")
    
    # 计算每个图片的哈希
    for img_path in tqdm(image_files):
        img_hash = get_image_hash(img_path, hash_size=hash_size)
        if img_hash:
            hashes[img_hash].append({
                "path": img_path,
                "size": os.path.getsize(img_path),
                "mtime": os.path.getmtime(img_path)
            })
    
    # 过滤出重复的组
    duplicates = [group for group in hashes.values() if len(group) > 1]
    return duplicates

def generate_report(duplicates, output_path="duplicates_report.json"):
    """生成重复图片报告"""
    report = {
        "total_duplicate_groups": len(duplicates),
        "total_duplicate_files": sum(len(g) for g in duplicates),
        "groups": duplicates
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"重复报告已保存到 {output_path}")
    return report

def delete_duplicates(duplicates, keep_newest=True):
    """删除重复图片，保留最新/最旧的版本"""
    total_deleted = 0
    total_saved_space = 0
    
    for group in duplicates:
        # 排序，决定保留哪一个
        if keep_newest:
            group_sorted = sorted(group, key=lambda x: x["mtime"], reverse=True)
        else:
            group_sorted = sorted(group, key=lambda x: x["mtime"])
        
        # 保留第一个，删除其余的
        keep = group_sorted[0]
        to_delete = group_sorted[1:]
        
        for item in to_delete:
            try:
                send2trash(item["path"])
                total_deleted += 1
                total_saved_space += item["size"]
                print(f"已移到回收站: {item['path']}")
            except Exception as e:
                print(f"删除失败 {item['path']}: {e}")
    
    print(f"\n清理完成：共删除 {total_deleted} 张重复图片，释放空间 {total_saved_space / 1024 / 1024:.2f} MB")
    return total_deleted, total_saved_space

def main():
    parser = argparse.ArgumentParser(description="AI 智能重复图片清理工具")
    parser.add_argument("directory", help="要扫描的图片目录")
    parser.add_argument("--threshold", type=int, default=0, help="相似度阈值 (0 为完全相同，数值越大允许的相似度越低)")
    parser.add_argument("--hash-size", type=int, default=16, help="哈希计算大小，数值越大精度越高")
    parser.add_argument("--report-only", action="store_true", help="仅生成报告，不执行删除")
    parser.add_argument("--keep", choices=["newest", "oldest"], default="newest", help="保留最新还是最旧的图片")
    parser.add_argument("--output", default="duplicates_report.json", help="报告输出路径")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"错误：目录 {args.directory} 不存在")
        return
    
    duplicates = find_duplicates(args.directory, args.threshold, args.hash_size)
    
    if not duplicates:
        print("没有找到重复图片")
        return
    
    print(f"\n找到 {len(duplicates)} 组重复图片，共 {sum(len(g) for g in duplicates)} 个重复文件")
    
    # 生成报告
    generate_report(duplicates, args.output)
    
    if args.report_only:
        return
    
    # 确认删除
    confirm = input("\n确认要删除重复图片吗？删除后文件会移到回收站 (y/N): ")
    if confirm.lower() == "y":
        delete_duplicates(duplicates, keep_newest=(args.keep == "newest"))
    else:
        print("已取消删除操作")

if __name__ == "__main__":
    main()
