"""dict 基础操作 — 创建、访问、设值、删除

直接运行：python 1_dict_basics.py
独立调用：python -c "from 1_dict_basics import demo_create; demo_create()"
"""


def demo_create():
    """字典的几种创建方式"""
    d1 = {"a": 1, "b": 2}
    d2 = dict(a=1, b=2)
    d3 = dict([("a", 1), ("b", 2)])
    d4 = dict.fromkeys(["a", "b"], 0)
    d5 = {k: v * 2 for k, v in d1.items()}
    print("字面量:", d1)
    print("关键字参数:", d2)
    print("可迭代对象:", d3)
    print("fromkeys:", d4)
    print("推导式:", d5)


def demo_access():
    """访问与安全取值"""
    d = {"name": "张三", "age": 25}

    # 直接取值（key 不存在会报 KeyError）
    print("d['name'] =", d["name"])

    # get — 安全取值
    print("get('name') =", d.get("name"))
    print("get('city') =", d.get("city"))        # None
    print("get('city', '未知') =", d.get("city", "未知"))

    # setdefault — 不存在则设默认值
    d.setdefault("city", "北京")
    d.setdefault("name", "李四")                  # name 已存在，不覆盖
    print("setdefault 后:", d)

    # in 检查
    print("'name' in d =", "name" in d)
    print("'gender' in d =", "gender" in d)


def demo_delete():
    """删除操作"""
    d = {"a": 1, "b": 2, "c": 3}

    # pop — 删除并返回值
    v = d.pop("a")
    print("pop('a') =", v, ", 剩余:", d)

    # pop 安全版
    v = d.pop("x", "没找到")
    print("pop('x', '没找到') =", v)

    # popitem — 弹出最后插入的项 (3.7+ LIFO)
    d["d"] = 4
    k, v = d.popitem()
    print("popitem() →", (k, v), ", 剩余:", d)

    # del
    del d["b"]
    print("del d['b'] 后:", d)


def demo_modify():
    """增改与清空"""
    d = {"a": 1}
    d["b"] = 2        # 新增
    d["a"] = 10       # 修改
    print("修改后:", d)
    d.clear()
    print("clear 后:", d)


if __name__ == "__main__":
    demo_create()
    print()
    demo_access()
    print()
    demo_delete()
    print()
    demo_modify()
