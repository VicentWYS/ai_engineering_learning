"""json.dumps 处理非标准类型 — default 参数"""

import json
from datetime import datetime
from decimal import Decimal


# 不可直接序列化的对象
data = {"time": datetime.now(), "price": Decimal("19.99")}

# ❌ 直接 dumps 会报 TypeError
try:
    json.dumps(data)
except TypeError as e:
    print(f"TypeError: {e}")

# ✅ 用 default 参数指定转换函数
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Unknown type: {type(obj)}")

print(json.dumps(data, default=custom_serializer, indent=2, ensure_ascii=False))

# ✅ 简写：直接用 str (datetime 会自动调 __str__)
print(json.dumps({"time": datetime.now()}, default=str, ensure_ascii=False))
