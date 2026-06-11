# try-except — Python 异常处理

## 一句话概括

`try-except` 是 Python 的结构化异常处理机制，用于捕获运行时错误并决定如何处理——是恢复、降级、重试，还是向上传播。它把"正常逻辑"和"错误处理逻辑"分离，避免业务代码被 `if err != nil` 淹没。

## 核心语法

```python
try:
    # 受保护的代码块
    result = risky_operation()
except ValueError as e:
    # 处理特定异常
    log(f"值错误: {e}")
except (KeyError, IndexError) as e:
    # 一次捕获多种异常
    fallback()
else:
    # try 块无异常时执行
    cache.set(result)
finally:
    # 无论是否异常，始终执行
    connection.close()
```

## 四个子句的职责

| 子句 | 何时执行 | 典型用途 |
|------|----------|----------|
| `try` | 始终执行（直到异常发生） | 放置可能出错的代码 |
| `except` | try 中发生匹配的异常时 | 捕获并处理特定错误 |
| `else` | try 中**没有**异常时 | 放"依赖 try 成功"的逻辑，避免误捕获 |
| `finally` | 无论是否异常都执行 | 释放资源（文件句柄、锁、连接） |

## 异常层级速查

```
BaseException
 ├── SystemExit          # sys.exit() 触发
 ├── KeyboardInterrupt   # Ctrl+C
 ├── GeneratorExit       # generator.close()
 └── Exception           # ← 绝大多数异常的父类
      ├── ArithmeticError
      │    ├── ZeroDivisionError
      │    └── OverflowError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── OSError
      │    ├── FileNotFoundError
      │    └── PermissionError
      ├── ValueError
      ├── TypeError
      ├── AttributeError
      ├── ImportError / ModuleNotFoundError
      ├── RuntimeError
      └── AssertionError         # assert 失败
```

> **警告**：永远不要 `except BaseException` 或裸 `except:`，这会吞掉 `KeyboardInterrupt` 和 `SystemExit`，导致程序无法正常退出。

## 常见反模式

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| `except:`（裸 except） | 吞掉所有异常包括 Ctrl+C | 至少用 `except Exception:` |
| `except Exception: pass` | 静默吞错，排查困难 | 至少 `log.exception()` |
| `try` 块太大 | 分不清哪行出错 | try 只包裹可能出错的最小范围 |
| `except` 后不指定变量 | 看不到异常信息 | `except X as e:` 保留上下文 |
| 在 `except` 中用 `raise` 不加 `from` | 丢失异常链 | 用 `raise ... from e` 或 `raise ... from None` |

## 关联语法

- `raise` — 主动抛出异常
- `raise ... from e` — 异常链：保留原始异常作为上下文
- `raise ... from None` — 抑制上下文，只抛出当前异常
- `with` 语句 — `try-finally` 的语法糖，自动调用 `__exit__`
- `assert` — 调试用条件检查，可用 `-O` 全局禁用
- `except*`（Python 3.11+）— 异常组处理

---

## 演进历史

| 版本 | 年份 | 变化 |
|------|------|------|
| Python 0.9.1 | 1991 | 首次引入 `try` / `except` 语法，使用 `except Name, description:` 的逗号语法捕获异常 |
| Python 1.5 | 1998 | 引入异常类层级结构（`Exception` 基类），`except` 可匹配子类。从此不再只能捕获"完全匹配"的异常 |
| Python 2.0 | 2000 | PEP 229 重构了异常处理在 C 层面的实现，`sys.exc_info()` 正式成为获取异常信息的标准方式 |
| Python 2.5 | 2006 | **里程碑**：`try/except/finally` 可以在同一个 `try` 块中同时使用。此前只能用 `try: ... except: ...` 再在外层嵌套 `try: ... finally: ...`。同版本引入 `with` 语句（PEP 343）作为 `try-finally` 的语法糖 |
| Python 2.6 | 2008 | `except Exc as e` 语法引入（`as` 替代逗号），逗号语法标记为废弃 |
| Python 3.0 | 2008 | **重大清理**：`raise Exc, arg` 和 `raise Exc, arg, tb` 语法移除，只保留 `raise Exc(arg)`；异常实例的 `message` 属性移除；所有异常必须是 BaseException 子类（不能 raise 字符串）；引入 `__traceback__` 属性 |
| Python 3.3 | 2012 | PEP 409：`raise ... from None` 语法，允许显式抑制异常链的 `__context__` |
| Python 3.11 | 2022 | PEP 654：引入 ExceptionGroup 和 `except*` 语法，一个 `except*` 可以捕获异常组中**部分**匹配项，未匹配的继续传播。同时引入 `add_note()` 方法（PEP 678），允许向异常附加多条备注信息 |
| Python 3.12 | 2023 | 改进 traceback 信息，`NameError` 等异常提供更精准的"你是不是想写……"建议 |

> **Python 2 → 3 迁移要点**：`except Exc, e` → `except Exc as e`；`raise "message"` → 不再合法；`except` 中 `raise` 默认自动携带原始 traceback（链式异常）。

---

## 历史故事：从错误码到异常——Ariane 5 火箭爆炸的教训

1996 年 6 月 4 日，法属圭亚那库鲁航天中心。欧洲航天局的 Ariane 5 火箭在发射后仅仅 37 秒就偏离轨道、启动自毁程序，化为火球坠入大西洋。损失：约 3.7 亿美元。事后调查结果令人震惊——罪魁祸首是**一个未处理的异常**。

Ariane 5 的惯性导航系统（SRI）里运行着从 Ariane 4 复用的软件代码。这段代码里有一个变量——水平速度的 64 位浮点值——被转换成了 16 位有符号整数。在 Ariane 4 时代，这个值永远不会超过 32767，所以转换从未出过问题。但 Ariane 5 的加速度更大，这个值首次超过了 16 位整数的上限。转换操作抛出了一个 `Operand Error`（相当于 Python 的 `OverflowError`）。

更致命的是，工程师在设计这条异常处理路径时做了一个看似合理的决定：如果 SRI 出故障，直接把异常信息输出到数据总线，然后……什么都不做。异常信息被主计算机解释为导航数据，于是火箭开始执行一个疯狂的转向——不是因为机械故障，而是因为错误信息被当成了飞行指令。

事后复盘报告里有一句话被软件工程领域反复引用："The exception was not caught because the specification did not identify it as an exception."（这个异常没有被捕获，因为规范文档没有标明它是异常。）换句话说，**代码有异常处理，但处理了错误的异常**。程序员可能加了 try-catch，却只捕获了"他们认为可能发生的错误"，对于"不可能发生"的边界条件，选择了无声吞掉。

这和今天 Python 社区的智慧完全一致：

1. **不要捕获你没准备好的异常**。捕获 `ValueError` 却对溢出类型一脸茫然，不如让它崩溃——至少崩溃有 traceback，不会把错误导航数据注入火箭。
2. **except 块不是"跳过错误"的工具**。它是"我知道这个错误意味着什么，且我知道如何恢复"的声明。不知道如何恢复？`raise` 向上传播。
3. **窄化 try 块**。如果 Ariane 团队把 try 块只包裹那行类型转换，而不是整个导航系统的初始化，故障定位可能只需要几分钟而非几个月。

此事之后，欧洲航天局修改了软件规范，要求所有异常必须被明确分类和处理。Python 社区的 `except Exception:` 而非裸 `except:` 的共识，异常链的 `raise ... from`，以及 3.11 的 ExceptionGroup，本质上都在回答同一个问题：**当程序偏离预期路径时，你如何确保错误信息不丢失、不错位、不被误导？**
