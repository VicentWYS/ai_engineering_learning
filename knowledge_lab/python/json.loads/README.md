# json.loads — JSON 字符串反序列化为 Python 对象

## 一句话概括

`json.loads(s, **kwargs)` 将 JSON 格式字符串解析为 Python 对象（`dict` → `dict`，`[...]` → `list`）。是 HTTP 响应体解析、配置文件读取、日志反查等场景的核心工具。

简单来说：将 JSON 字符串还原成 Python 字典/列表。

## 签名

```python
json.loads(s, *, cls=None, object_hook=None, parse_float=None,
           parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)
```

## 常用参数速查

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `object_hook` | `None` | 传入函数，对每个 `dict` 调用，返回值替代原 `dict`。常用于将字典转为自定义对象（如 `User` dataclass） |
| `object_pairs_hook` | `None` | 与 `object_hook` 类似，但接收 `(key, value)` 对列表，可保留插入顺序或处理重复 key |
| `parse_float` | `float` | 自定义浮点数解析器，如用 `Decimal` 替代 `float` 避免精度丢失 |
| `parse_int` | `int` | 自定义整数解析器，如限制超大整数、或改用 `Decimal` |
| `parse_constant` | 内置处理 | 处理 `NaN`、`Infinity`、`-Infinity`。可传入工厂函数或抛异常拒绝这些值 |
| `cls` | `JSONDecoder` | 传入自定义 `JSONDecoder` 子类，高级用法 |

> **注意**：`object_pairs_hook` 优先级高于 `object_hook`。如果同时指定，`object_hook` 会被忽略。

## 常见用法示例

```python
import json

# 基础用法
json.loads('{"name": "张三", "age": 25}')
# {'name': '张三', 'age': 25}

# 数组 JSON
json.loads('[1, 2, 3]')
# [1, 2, 3]

# 用 object_hook 转为自定义对象
def as_user(d):
    return User(**d)

json.loads('{"name": "张三", "age": 25}', object_hook=as_user)

# 用 Decimal 解析浮点数（避免精度丢失）
from decimal import Decimal
json.loads('{"price": 19.99}', parse_float=Decimal)
# {'price': Decimal('19.99')}
```

## 类型映射（JSON → Python）

| JSON | Python |
|------|--------|
| `object` (`{...}`) | `dict` |
| `array` (`[...]`) | `list` |
| `string` | `str` |
| `number` (int) | `int` |
| `number` (float) | `float`（可通过 `parse_float` 覆盖） |
| `true` / `false` | `True` / `False` |
| `null` | `None` |
| `NaN` / `Infinity` | `float('nan')` / `float('inf')`（可通过 `parse_constant` 拦截） |

## 关联函数

- `json.load(fp)` — 直接从文件流读取并反序列化
- `json.dumps(obj)` — 将 Python 对象序列化为 JSON 字符串
- `json.dump(obj, fp)` — 序列化并写入文件流

---

## 演进历史

| 版本 | 年份 | 变化 |
|------|------|------|
| Python 2.6 | 2008 | `json` 模块随 `simplejson` 合并进入标准库，`loads` 作为四个核心函数之一（`dumps`/`dump`/`loads`/`load`）正式提供 |
| Python 2.7 | 2010 | 新增 `object_pairs_hook` 参数，允许以 `(key, value)` 对列表形式接收 dict，用于保留顺序和处理重复 key。同时 `parse_constant` 文档明确说明可拦截 `NaN`/`Infinity` |
| Python 3.1 | 2009 | `json.loads` 在 Python 3 中开始接受 `str` 类型（Python 2 中接受 `str` 即字节串，行为不一致的问题被修复） |
| Python 3.3 | 2012 | `parse_constant` 行为细化：默认处理 `-Infinity` 字符串，此前部分版本对该值的处理未明确 |
| Python 3.4 | 2014 | C 扩展加速器默认启用，`loads` 解析速度提升 10-20 倍。`object_pairs_hook` 的效率也随之优化 |
| Python 3.6 | 2016 | CPython dict 实现改为有序，`json.loads` 默认结果保持 JSON 中 key 的插入顺序（但从规范角度，仍推荐用 `object_pairs_hook` 显式控制顺序） |
| Python 3.7 | 2018 | dict 插入顺序保留成为语言规范，`json.loads` 的行为因此更可预测 |

> **Python 2 → 3 迁移注意**：Python 2 中 `json.loads` 接受 `str`（字节串），Python 3 中只接受 `str`（Unicode）。传入 `bytes` 会直接抛出 `TypeError`，这是最常见的迁移坑之一。

---

## 历史故事：为什么 eval() 是魔鬼，json.loads 是救兵

2005 年，AJAX 技术让 Web 应用焕然一新。前端 JavaScript 用 `XMLHttpRequest` 拿到后端数据，然后更新页面——不需要刷新！但拿到的是什么数据呢？XML 又慢又啰嗦，于是大家开始用 JSON。

JavaScript 端很简单：`eval("(" + jsonString + ")")` 一行搞定。快是快，但 `eval` 是个定时炸弹——它能执行**任意 JavaScript 代码**。假如服务器返回的 JSON 被中间人篡改，植入了恶意脚本，浏览器会直接执行它。这在 XSS（跨站脚本攻击）盛行的年代简直是灾难。

于是 Douglas Crockford 站出来写了一篇著名的文章《JSON：无脂肪的 XML 替代品》，并发布了一个 JS 库：`json2.js`。它的核心创新是——**增加了一个解析器**。这个解析器只认 JSON 语法规范的那几个字面量（`{}`、`[]`、`"`、数字、布尔），拒绝任何可执行代码。2006 年 Bob Ippolito 给 Python 写了 `simplejson`，2008 年进标准库。

`json.loads` 的核心设计哲学就是这一点：**它能解析的，只是数据。不是代码。** 你永远不用担心 `json.loads(response.text)` 会像 `eval()` 一样悄悄执行 `__import__('os').system('rm -rf /')`。JSON 解析器是一个**纯数据解码器**，它在语法层面就拒绝了可执行逻辑的存在。

这个设计原则影响深远。今天几乎所有编程语言标准库里的 JSON 解析器都遵循同一套安全边界：JSON 是数据格式，不是代码格式。当你写下 `data = json.loads(http_response_text)` 时，你得到的一定是安全的 Python 字典/列表——不会多也不会少。

另外值得一提的是 `object_pairs_hook` 的设计。它的诞生来自一个真实需求：JSON 规范说 object 是无序的键值对集合，但实际业务中 order matters——配置文件里的键顺序、API 返回的字段排列，开发者希望保留。于是 Python 社区在 2.7 时代加入了这个 hook，让你既能按标准解析 JSON，又能在需要时精确控制键的顺序。这种"标准兼容 + 实用扩展"的设计，是 Python 标准库一贯的风格。
