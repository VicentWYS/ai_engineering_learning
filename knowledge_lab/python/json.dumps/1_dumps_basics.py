"""json.dumps 快速验证脚本"""

import json

data = {"name": "张三", "age": 25, "hobbies": ["钓鱼", "编程"], "active": True, "score": None}

# 1. 默认行为（中文被转义）
print("=== 默认 ===")
print(json.dumps(data))

# 2. 保留中文
print("\n=== ensure_ascii=False ===")
print(json.dumps(data, ensure_ascii=False))

# 3. 美化输出
print("\n=== indent=2 ===")
print(json.dumps(data, indent=2, ensure_ascii=False))

# 4. 紧凑输出
print("\n=== 紧凑 ===")
print(json.dumps(data, separators=(",", ":"), ensure_ascii=False))

# 5. 排序 key
print("\n=== sort_keys=True ===")
print(json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False))
