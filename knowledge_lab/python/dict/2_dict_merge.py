"""dict 合并与推导 — update、| 运算、** 解包、字典推导

直接运行：python 2_dict_merge.py
独立调用：python -c "from 2_dict_merge import demo_update; demo_update()"
"""


def demo_update():
    """update — 将另一个字典的键值对写入"""
    d = {"a": 1, "b": 2}
    d.update({"b": 20, "c": 3})
    print("update 后:", d)  # b 被覆盖，c 新增


def demo_pipe_merge():
    """| 运算符合并 — Python 3.9+，后者覆盖前者"""
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 20, "c": 3}
    merged = d1 | d2
    print("d1 | d2 =", merged)   # 新字典
    print("d1 未变:", d1)


def demo_pipe_update():
    """|= 原地合并 — Python 3.9+"""
    d1 = {"a": 1, "b": 2}
    d1 |= {"b": 20, "c": 3}
    print("d1 |= 后:", d1)


def demo_star_unpack():
    """** 解包合并 — Python 3.5+"""
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 20, "c": 3}
    merged = {**d1, **d2}
    print("{**d1, **d2} =", merged)


def demo_comprehension():
    """字典推导式"""
    d = {"a": 1, "b": 2, "c": 3}
    # 翻转 key-value
    flipped = {v: k for k, v in d.items()}
    # 过滤
    filtered = {k: v for k, v in d.items() if v > 1}
    # 变换 value
    doubled = {k: v * 2 for k, v in d.items()}
    print("翻转:", flipped)
    print("过滤(v>1):", filtered)
    print("翻倍:", doubled)


if __name__ == "__main__":
    demo_update()
    print()
    demo_pipe_merge()
    print()
    demo_pipe_update()
    print()
    demo_star_unpack()
    print()
    demo_comprehension()
