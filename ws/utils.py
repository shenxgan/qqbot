import os
import hashlib


def get_files_hash(directory):
    """计算目录下所有 .py 文件的哈希值"""
    hasher = hashlib.md5()
    for filename in sorted(os.listdir(directory)):  # 排序保证一致性
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "rb") as f:
                    hasher.update(f.read())  # 计算文件内容的哈希
            except Exception as e:
                print(f"无法读取 {filepath}: {e}")
    return hasher.hexdigest()
