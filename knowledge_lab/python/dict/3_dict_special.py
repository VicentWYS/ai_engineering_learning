"""dict 高级用法 — defaultdict、Counter、OrderedDict、视图遍历

直接运行：python 3_dict_special.py
独立调用：python -c "from 3_dict_special import demo_defaultdict; demo_defaultdict()"
"""

from collections import defaultdict, Counter, OrderedDict, ChainMap


def demo_defaultdict():
    """defaultdict — 访问不存在的 key 时自动生成默认值"""
    d = defaultdict(int)
    words = ["a", "b", "a", "c", "b", "a"]
    for w in words:
        d[w] += 1                  # 不需要 if w not in d
    print("defaultdict(int) 计数:", dict(d))

    d2 = defaultdict(list)
    d2["fruits"].append("苹果")
    d2["fruits"].append("香蕉")
    print("defaultdict(list):", dict(d2))


def demo_counter():
    """Counter — 计数器，统计元素出现次数"""
    c = Counter("abracadabra")
    print("Counter('abracadabra'):", c)
    print("最常见的 3 个:", c.most_common(3))
    print("各元素:", list(c.elements()))

    # 支持数学运算
    c2 = Counter("abc")
    print("+ :", c + c2)
    print("- :", c - c2)


def demo_ordereddict():
    """OrderedDict — 有序字典（3.7+ 普通 dict 已有序，两者差异很小）"""
    od = OrderedDict()
    od["a"] = 1
    od["b"] = 2
    od["c"] = 3
    print("OrderedDict:", od)

    # OrderedDict 独有的方法
    od.move_to_end("a")            # 移到末尾
    print("move_to_end('a'):", od)
    od.move_to_end("c", last=False)  # 移到开头
    print("move_to_end('c', last=False):", od)

    # 相等比较对顺序敏感
    od2 = OrderedDict(a=1, b=2, c=3)
    print("od == od2:", od == od2)  # 顺序不同 → False


def demo_chainmap():
    """ChainMap — 将多个字典链接起来查找"""
    defaults = {"host": "localhost", "port": 8080}
    cli_args = {"port": 3000}
    env_vars = {"host": "prod.example.com", "debug": "true"}

    config = ChainMap(cli_args, env_vars, defaults)
    print("host:", config["host"])     # cli_args 优先
    print("port:", config["port"])     # cli_args 优先
    print("debug:", config["debug"])   # env_vars
    print("完整映射:", dict(config))


def demo_views():
    """keys/values/items 视图 — 实时反映字典变化"""
    d = {"a": 1, "b": 2}
    keys = d.keys()
    values = d.values()

    print("修改前 keys:", list(keys))
    d["c"] = 3
    print("新增后 keys:", list(keys))   # 视图实时更新

    # 视图支持集合操作
    d2 = {"b": 20, "c": 30}
    print("& 交集:", d.keys() & d2.keys())
    print("| 并集:", d.keys() | d2.keys())
    print("- 差集:", d.keys() - d2.keys())
    print("^ 对称差:", d.keys() ^ d2.keys())


if __name__ == "__main__":
    demo_defaultdict()
    print()
    demo_counter()
    print()
    demo_ordereddict()
    print()
    demo_chainmap()
    print()
    demo_views()
