"""json.loads 的 object_hook 和 object_pairs_hook 快速验证"""

import json
from dataclasses import dataclass


# ---- object_hook: dict → 自定义对象 ----


@dataclass
class User:
    name: str
    age: int


def demo_object_hook():
    """用 object_hook 将 dict 转为 dataclass / 自定义对象"""
    s = '{"name": "张三", "age": 25}'

    # 无 hook：得到普通 dict
    result = json.loads(s)
    print(f"无 hook: {type(result).__name__} = {result}")

    # 有 hook：转为 User 对象
    user = json.loads(s, object_hook=lambda d: User(**d))
    print(f"有 hook: {type(user).__name__} = {user}")
    print(f"  user.name = {user.name}, user.age = {user.age}")


def demo_nested_object_hook():
    """object_hook 作用于每一层嵌套 dict"""
    s = '''
    {
        "user": {"name": "张三", "age": 25},
        "meta": {"source": "api", "version": 1}
    }
    '''

    def hook(d):
        # 有 "name" 和 "age" 的转为 User，否则保留普通 dict
        if "name" in d and "age" in d:
            return User(**d)
        return d

    result = json.loads(s, object_hook=hook)
    print(f"外层: {type(result).__name__}")
    print(f"  result['user']: {type(result['user']).__name__} = {result['user']}")
    print(f"  result['meta']: {type(result['meta']).__name__} = {result['meta']}")


# ---- object_pairs_hook: 保留顺序 / 处理重复 key ----


def demo_object_pairs_hook_order():
    """object_pairs_hook 接收 (key, value) 对列表，可精确控制顺序"""
    s = '{"z": 1, "a": 2, "m": 3}'

    # 默认：Python 3.7+ 保留 JSON 中 key 的顺序
    default = json.loads(s)
    print(f"默认顺序: {list(default.keys())}")

    # object_pairs_hook：显式控制顺序
    from collections import OrderedDict
    ordered = json.loads(s, object_pairs_hook=OrderedDict)
    print(f"OrderedDict: {list(ordered.keys())}")
    print(f"  类型: {type(ordered).__name__}")


def demo_duplicate_keys():
    """处理 JSON 中有重复 key 的情况（JSON 规范不建议，但现实中存在）"""
    s = '{"key": "first", "key": "second", "key": "third"}'

    # object_pairs_hook 可以检测到重复
    def detect_duplicates(pairs):
        seen = set()
        for k, v in pairs:
            if k in seen:
                print(f"  检测到重复 key: {k!r}")
            seen.add(k)
        return dict(pairs)

    result = json.loads(s, object_pairs_hook=detect_duplicates)
    print(f"最终取值: {result}")  # Python 默认保留最后一个值


def demo_pairs_hook_priority():
    """object_pairs_hook 优先级高于 object_hook，二者同时指定时 object_hook 被忽略"""
    s = '{"name": "李四", "age": 30}'

    result = json.loads(
        s,
        object_hook=lambda d: User(**d),  # 这个会被忽略!
        object_pairs_hook=lambda pairs: dict(pairs),
    )
    print(f"object_hook 被忽略: {type(result).__name__} = {result}")


if __name__ == "__main__":
    demo_object_hook()
    print()
    demo_nested_object_hook()
    print()
    demo_object_pairs_hook_order()
    print()
    demo_duplicate_keys()
    print()
    demo_pairs_hook_priority()
