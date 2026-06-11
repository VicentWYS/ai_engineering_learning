"""异常层级、捕获顺序与反模式验证"""


def exception_hierarchy():
    """验证异常继承关系（Exception → 具体异常）"""
    print("=== 异常类继承关系 ===")
    exceptions = [
        ZeroDivisionError, ValueError, IndexError, KeyError,
        FileNotFoundError, TypeError, AttributeError, RuntimeError
    ]
    for exc in exceptions:
        bases = [b.__name__ for b in exc.__mro__]
        chain = " → ".join(bases[:5])
        print(f"  {exc.__name__:25s}: {chain}")


def catch_order():
    """捕获顺序：必须从具体到宽泛，否则宽泛的会先吞掉"""
    print("\n=== 捕获顺序：具体 → 宽泛 ===")
    try:
        raise ZeroDivisionError("测试")
    except ArithmeticError:  # ZeroDivisionError 的父类，先匹配
        print("  ArithmeticError 先捕获（子类 ZeroDivisionError 没机会了）")
    except ZeroDivisionError:
        print("  ← 永远不会执行")


def wide_catch_danger():
    """裸 except: 会吞掉 KeyboardInterrupt 和 SystemExit"""
    print("\n=== 裸 except 的危险性 ===")
    try:
        raise SystemExit(1)
    except BaseException as e:
        print(f"  except BaseException 捕获: {type(e).__name__}")
        print("  （SystemExit 被吞，程序本该退出但继续执行了）")

    print("\n=== 正确：只捕获 Exception ===")
    import sys
    try:
        1 / 0
    except Exception as e:
        print(f"  except Exception 捕获: {type(e).__name__}")
        print("  （不会拦截 SystemExit / KeyboardInterrupt）")


def catch_oserror():
    """OSError 家族：Python 3.3+ 合并了多种 IO 异常"""
    print("\n=== OSError 家族 ===")
    for cls in [FileNotFoundError, PermissionError,
                TimeoutError, ConnectionError, OSError]:
        print(f"  {cls.__name__:25s} → 父类: {cls.__bases__[0].__name__}")


def empty_except_demo():
    """演示 except Exception: pass 的调试困境"""
    print("\n=== except ... pass 的代价 ===")

    def dangerous_silence(data):
        try:
            return data["key"] / 0
        except Exception:
            pass  # 什么都看不见

    result = dangerous_silence({"key": 10})
    print(f"  返回: {result!r}（到底是 KeyError 还是 ZeroDivisionError？查不出来）")


if __name__ == "__main__":
    exception_hierarchy()
    catch_order()
    wide_catch_danger()
    catch_oserror()
    empty_except_demo()
