"""raise、异常链与自定义异常验证"""

import traceback


def basic_raise():
    """主动抛出异常"""
    print("=== 主动 raise ===")
    try:
        raise ValueError("参数不合法")
    except ValueError as e:
        print(f"  捕获: {e}")


def raise_from_chaining():
    """raise ... from e：保留完整异常链"""
    print("\n=== raise ... from e 异常链 ===")
    try:
        try:
            d = {}
            d["missing"]
        except KeyError as e:
            raise RuntimeError("配置加载失败") from e
    except RuntimeError as e:
        print(f"  最终异常: {type(e).__name__}: {e}")
        print(f"  原始异常 __cause__: {type(e.__cause__).__name__}: {e.__cause__}")


def raise_from_none():
    """raise ... from None：显式断开异常链"""
    print("\n=== raise ... from None 断开链 ===")
    try:
        try:
            1 / 0
        except ZeroDivisionError:
            raise RuntimeError("内部错误") from None
    except RuntimeError as e:
        print(f"  异常: {type(e).__name__}: {e}")
        print(f"  __cause__: {e.__cause__}（None，链已断开）")
        print(f"  __context__: {type(e.__context__).__name__}（隐式上下文仍在）")


def implicit_chaining():
    """除 from 外，except 中 raise 会自动设置 __context__"""
    print("\n=== 隐式异常链（__context__） ===")
    try:
        try:
            int("abc")
        except ValueError as e:
            raise TypeError("类型转换二次失败")  # 没有 from，__context__ 自动设置
    except TypeError as e:
        print(f"  异常: {e}")
        print(f"  __context__: {type(e.__context__).__name__}: {e.__context__}")


def custom_exception():
    """自定义异常类"""
    print("\n=== 自定义异常 ===")

    class ConfigError(Exception):
        """配置相关异常基类"""
        pass

    class ConfigNotFoundError(ConfigError):
        """配置项未找到"""

        def __init__(self, key, file=None):
            self.key = key
            self.file = file
            super().__init__(f"key={key!r} not found" + (f" in {file}" if file else ""))

    try:
        raise ConfigNotFoundError("api_key", file=".env")
    except ConfigNotFoundError as e:
        print(f"  异常类型: {type(e).__name__}")
        print(f"  消息: {e}")
        print(f"  属性 key={e.key}, file={e.file}")
        print(f"  是 ConfigError 子类: {isinstance(e, ConfigError)}")


def assert_demo():
    """assert 用于调试，可用 -O 禁用"""
    print("\n=== assert 调试断言 ===")

    def divide_with_assert(a, b):
        assert b != 0, "除数不能为零"
        return a / b

    print(f"  divide_with_assert(10, 2) = {divide_with_assert(10, 2)}")
    try:
        divide_with_assert(10, 0)
    except AssertionError as e:
        print(f"  AssertionError: {e}")


def exception_notes():
    """Python 3.11+ add_note() 附加备注"""
    print("\n=== add_note() 附加信息（3.11+） ===")
    import sys
    if sys.version_info < (3, 11):
        print("  当前 Python 版本不支持 add_note()，需要 3.11+")
        return

    try:
        raise ValueError("数据校验失败")
    except ValueError as e:
        e.add_note("发生于: 第 3 行用户输入")
        e.add_note("建议: 检查输入格式")
        traceback.print_exc()


if __name__ == "__main__":
    basic_raise()
    raise_from_chaining()
    raise_from_none()
    implicit_chaining()
    custom_exception()
    assert_demo()
    exception_notes()
