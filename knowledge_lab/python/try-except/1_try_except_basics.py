"""try-except 基础语法快速验证"""


def basic_try_except():
    """最基础的 try-except：捕获特定异常"""
    print("=== 基础捕获 ZeroDivisionError ===")
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        print(f"捕获到: {type(e).__name__}: {e}")


def multiple_except():
    """一个 try 对应多个 except，按顺序匹配"""
    print("=== 多个 except 分支 ===")
    cases = [lambda: 1 / 0, lambda: int("abc"), lambda: [][0]]
    for i, case in enumerate(cases):
        try:
            case()
        except ZeroDivisionError:
            print(f"  case{i}: 除零错误")
        except ValueError:
            print(f"  case{i}: 值错误")
        except IndexError:
            print(f"  case{i}: 索引越界")


def except_tuple():
    """一个 except 捕获多种异常"""
    print("=== except (A, B, C) 一次捕获多种 ===")
    for value in ["1/0", "abc", "[][0]"]:
        try:
            if value == "1/0":
                1 / 0
            elif value == "abc":
                int("abc")
            else:
                [][0]
        except (ZeroDivisionError, ValueError, IndexError) as e:
            print(f"  {value}: {type(e).__name__}")


def else_clause():
    """else 子句：try 无异常时执行，不被 except 覆盖"""
    print("=== else 子句 ===")

    def divide(a, b):
        try:
            result = a / b
        except ZeroDivisionError:
            print(f"  {a}/{b}: 除数不能为零")
        else:
            print(f"  {a}/{b} = {result}（else 被执行）")

    divide(10, 2)
    divide(10, 0)


def finally_clause():
    """finally 子句：无论是否异常都执行"""
    print("=== finally 子句 ===")

    def demo(should_fail):
        try:
            print("  try 开始")
            if should_fail:
                1 / 0
            print("  try 正常结束")
        except ZeroDivisionError:
            print("  except 捕获异常")
        finally:
            print("  finally 执行（资源释放）")
        print("  函数结束\n")

    demo(False)
    demo(True)


def finally_shortcut():
    """finally 中的 return 会吞掉异常"""
    print("=== finally 中的 return 吞掉异常 ===")

    def bad_practice():
        try:
            raise ValueError("原始错误")
        finally:
            return "finally 的返回值"  # 异常被吞掉

    result = bad_practice()
    print(f"  返回值: {result}（异常被静默丢弃！）")


def scope_note():
    """except 块结束后，异常变量被删除（避免循环引用）"""
    print("=== except 变量作用域 ===")
    try:
        1 / 0
    except ZeroDivisionError as e:
        saved = str(e)
        print(f"  except 内可访问 e: {saved}")

    try:
        print(f"  except 外: {e}")
    except NameError:
        print("  except 外 e 已被删除（NameError）")


if __name__ == "__main__":
    basic_try_except()
    print()
    multiple_except()
    print()
    except_tuple()
    print()
    else_clause()
    print()
    finally_clause()
    print()
    finally_shortcut()
    print()
    scope_note()
