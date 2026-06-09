"""json.loads 的 parse_float / parse_int / parse_constant 快速验证"""

import json
from decimal import Decimal


# ---- parse_float ----


def demo_parse_float_decimal():
    """用 Decimal 解析浮点数，避免 float 精度丢失"""
    s = '{"price": 19.99, "tax": 2.45}'

    # 默认 float：可能有精度问题
    default = json.loads(s)
    print(f"默认 float: price={default['price']!r}, 0.1+0.2={0.1+0.2!r}（float 精度问题示例）")

    # 用 Decimal：精确十进制
    result = json.loads(s, parse_float=Decimal)
    print(f"Decimal: price={result['price']!r}, tax={result['tax']!r}")
    print(f"  price + tax = {result['price'] + result['tax']!r}（精确计算）")


def demo_parse_float_round():
    """自定义 parse_float：保留两位小数"""
    s = '[3.14159, 2.71828, 1.61803]'

    result = json.loads(s, parse_float=lambda x: round(float(x), 2))
    print(f"四舍五入到两位: {result}")


# ---- parse_int ----


def demo_parse_int():
    """自定义 parse_int：限制整数范围、或改用 Decimal"""
    s = '{"small": 42, "large": 999999999999999999999999999}'

    # 默认 int
    default = json.loads(s)
    print(f"默认 int: small={default['small']!r}, large={default['large']!r}")

    # 全用 Decimal（避免超大整数）
    result = json.loads(s, parse_int=Decimal)
    print(f"Decimal: small={result['small']!r} (type={type(result['small']).__name__})")

    # 限制整数上限
    def capped_int(x):
        n = int(x)
        if n > 2**31 - 1:
            print(f"  警告: {n} 超过 int32 范围，保持为 int")
        return n

    json.loads(s, parse_int=capped_int)


# ---- parse_constant ----


def demo_parse_constant():
    """处理 JSON 中的 NaN / Infinity / -Infinity"""
    # 注意：JSON 规范严格来说不允许 NaN/Infinity，但 Python 的 json 模块默认支持
    s = '[NaN, Infinity, -Infinity, 42]'

    # 默认：转为 float('nan') / float('inf')
    default = json.loads(s)
    print(f"默认: {default}")
    import math
    print(f"  第一个是 NaN? {math.isnan(default[0])}")
    print(f"  第二个是 inf? {math.isinf(default[1])}")

    # 拒绝 NaN/Infinity（严格模式）
    def strict_constant(val):
        raise ValueError(f"不允许特殊值: {val}")

    try:
        json.loads(s, parse_constant=strict_constant)
    except ValueError as e:
        print(f"\n严格模式拦截: {e}")


# ---- 组合使用：金融场景 ----


def demo_finance_scenario():
    """模拟金融数据解析：Decimal 解析数字 + 拒绝 NaN"""
    s = '{"amount": 100.50, "rate": 0.05}'

    result = json.loads(
        s,
        parse_float=Decimal,
        parse_int=Decimal,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"非法值: {x}")),
    )
    interest = result["amount"] * result["rate"]
    print(f"金额: {result['amount']!r}, 利率: {result['rate']!r}")
    print(f"利息: {interest!r}（精确 Decimal）")


if __name__ == "__main__":
    demo_parse_float_decimal()
    print()
    demo_parse_float_round()
    print()
    demo_parse_int()
    print()
    demo_parse_constant()
    print()
    demo_finance_scenario()
