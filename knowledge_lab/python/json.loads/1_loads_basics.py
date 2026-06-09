"""json.loads 基础反序列化快速验证"""

import json


def basic_loads():
    """最基础的 JSON 字符串 → Python 对象"""
    # dict
    print("=== JSON对象 → dict ===")
    obj = json.loads('{"name": "张三", "age": 25, "active": true, "score": null}')
    print(f"type: {type(obj).__name__}, value: {obj}")

    # list
    print("\n=== JSON数组 → list ===")
    arr = json.loads('[1, 2, 3, "hello"]')
    print(f"type: {type(arr).__name__}, value: {arr}")

    # 嵌套结构
    print("\n=== 嵌套结构 ===")
    nested = json.loads('{"users": [{"name": "Alice"}, {"name": "Bob"}], "count": 2}')
    print(nested["users"][0]["name"])  # Alice


def type_mapping():
    """验证 JSON 类型 → Python 类型的对应关系"""
    s = '''
    {
        "str_val": "hello",
        "int_val": 42,
        "float_val": 3.14,
        "bool_true": true,
        "bool_false": false,
        "null_val": null,
        "list_val": [1, 2, 3],
        "nested": {"key": "value"}
    }
    '''
    obj = json.loads(s)
    for k, v in obj.items():
        print(f"{k:15s} → {type(v).__name__:10s} = {v!r}")


def loads_vs_eval():
    """对比 json.loads 和 eval 的安全性差异"""
    # json.loads 拒绝非 JSON 语法
    print("=== json.loads 拒绝执行代码 ===")
    malicious = '{"key": __import__("os").system("echo hacked")}'
    try:
        json.loads(malicious)
    except json.JSONDecodeError as e:
        print(f"安全拦截: {e}")

    # eval 会执行（危险! 仅演示不要在生产代码中使用）
    print("\n=== eval 会执行任意代码（危险!） ===")
    print(">>> eval('__import__(\"os\").getcwd()')  # 这行代码不会运行，仅为演示")


def error_handling():
    """常见解析错误类型"""
    cases = [
        ("缺少引号", "{name: value}"),
        ("尾部逗号", '{"name": "张三",}'),
        ("单引号", "{'name': '张三'}"),
        ("bytes 输入", b'{"name": "test"}'),
    ]
    for label, s in cases:
        try:
            json.loads(s)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"[{label}] {type(e).__name__}: {e}")


if __name__ == "__main__":
    basic_loads()
    print("\n" + "=" * 50 + "\n")
    type_mapping()
    print("\n" + "=" * 50 + "\n")
    loads_vs_eval()
    print("\n" + "=" * 50 + "\n")
    error_handling()
