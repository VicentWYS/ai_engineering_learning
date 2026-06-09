# json.dumps — Python 对象序列化为 JSON 字符串

## 一句话概括

`json.dumps(obj, **kwargs)` 将 Python 对象序列化为 JSON 格式的字符串。常用于构造 HTTP 请求体、写入文件、日志格式化等场景。
简单来说：将 Python 字典转换成 JSON 字符串。


## 签名

```python
json.dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True,
           allow_nan=True, cls=None, indent=None, separators=None,
           default=None, sort_keys=False, **kw)
```

## 常用参数速查

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `indent` | `None` | 缩进空格数，设为 `2` 或 `4` 可美化输出 |
| `ensure_ascii` | `True` | `True` 时将非 ASCII 字符转为 `\uXXXX`；设为 `False` 可保留中文原文 |
| `sort_keys` | `False` | `True` 时按 key 排序输出 |
| `separators` | `(', ', ': ')` | 设为 `(',', ':')` 可生成最紧凑的输出 |
| `default` | `None` | 传入函数处理 `datetime`、`Decimal` 等不可直接序列化的对象 |
| `skipkeys` | `False` | `True` 时跳过非 `str/int/float/bool/None` 的 dict key |

## 常见用法示例

```python
import json

data = {"name": "张三", "age": 25, "hobbies": ["钓鱼", "编程"]}

# 基础用法
json.dumps(data)
# '{"name": "\\u5f20\\u4e09", ...}'

# 保留中文
json.dumps(data, ensure_ascii=False)
# '{"name": "张三", ...}'

# 美化输出
json.dumps(data, indent=2, ensure_ascii=False)

# 紧凑输出（适合网络传输）
json.dumps(data, separators=(',', ':'), ensure_ascii=False)
```

## 类型映射

| Python | JSON |
|--------|------|
| `dict` | `object` |
| `list`, `tuple` | `array` |
| `str` | `string` |
| `int`, `float` | `number` |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

非上表类型（如 `datetime`、`Decimal`）需通过 `default` 参数指定转换函数，否则抛出 `TypeError`。

## 关联函数

- `json.dump(obj, fp)` — 直接写入文件流，不返回字符串
- `json.loads(s)` — 将 JSON 字符串反序列化为 Python 对象
- `json.load(fp)` — 从文件流读取并反序列化

---

## 演进历史

| 版本 | 年份 | 变化 |
|------|------|------|
| Python 2.6 | 2008 | `json` 模块被正式纳入标准库，基于 Bob Ippolito 开发的 `simplejson`。最初提供了 `dumps`/`dump`/`loads`/`load` 四个核心函数 |
| Python 3.1 | 2009 | 新增 `sort_keys` 参数，支持按键排序输出 |
| Python 3.3 | 2012 | `json.dumps` 的 `ensure_ascii` 开始默认 `True`（Python 2 中曾因字符串类型混乱而行为不一致） |
| Python 3.4 | 2014 | `json` 模块的 C 扩展加速在 CPython 中默认启用，`dumps` 性能大幅提升 |
| Python 3.5 | 2015 | `json.dumps` 开始支持 `indent` 为非负整数，不再仅限于 `None` 或非负整数 |
| Python 3.6 | 2016 | `json.dumps` 保留字典的插入顺序（得益于 CPython 3.6 的 dict 实现变化） |
| Python 3.7 | 2018 | 字典插入顺序保留成为语言规范，`json.dumps` 行为随之正式确定 |
| Python 3.9 | 2020 | `json.dumps(separators=(',', ':'))` 的紧凑模式在文档中被明确推荐用于网络传输场景 |

> Python 2 到 3 的最大差异：Python 2 中 `json.dumps` 接受的 `str` 是字节串，Python 3 中是 Unicode 字符串。迁移时最常见的坑是 `ensure_ascii=True`（默认）导致中文被转义。

---

## 历史故事：JSON 的诞生

2001 年，一个名叫 Douglas Crockford 的程序员正在做 Web 开发。那时浏览器和服务器之间传输数据的主流格式是 XML，但他觉得 XML 太重了——标签比数据还多，解析起来又慢又烦。

某天他发现 JavaScript 里有个取巧的办法：把数据写成 JS 对象字面量的样子，然后用 `eval()` 直接执行。这招很快，但 `eval` 能执行任意代码，安全风险极大。于是他写了一个小解析器，只解析数据子集，拒绝了可执行代码。他把这套格式称为 **JSON (JavaScript Object Notation)**。

JSON 真正引爆是在 2005 年，AJAX 技术兴起，前端需要一种轻量级格式跟后端交换数据。JSON 比 XML 精简得多，解析也快，一下子成了 Web 开发的事实标准。后来 API 设计（RESTful API）兴起，JSON 几乎成了 HTTP 通信的唯一选择。

Python 这边，Bob Ippolito 在 2006 年写了 `simplejson` 库，实现了 JSON 的编解码。因为太好用，社区呼声很高，2008 年 Python 2.6 把它收编进了标准库，改名就叫 `json`。今天几乎所有 Python HTTP 请求、配置文件、日志输出里，`json.dumps` 都在默默地工作。

你代码里那行 `json.dumps(payload_dict)`，本质上就是在用 Crockford 二十多年前发明的格式，把 Python 字典翻译成服务器能看懂的语言——一段纯文本，通过网线发出去，被另一端的程序准确无误地还原成它那边的数据结构。
