# 知识实验室

从代码中提取知识点，便于回顾与巩固。每个模块包含一个 `README.md`（概念讲解 + 历史故事）和一个 `main.py`（代码演示）。

## 目录

### AI 工程化
- [python-dotenv 环境变量管理](AI工程化/01_python-dotenv环境变量管理/README.md) — `load_dotenv()` 为什么是行业标准
- [OpenAI 接口规范](AI工程化/02_openai接口规范/README.md) — Chat Completions API 如何成为大模型调用的"统一语言"

### 编码与字符集
- [Windows 终端 UTF-8 编码](编码与字符集/01_windows终端utf-8编码/README.md) — 为什么 emoji 在 cmd.exe 里会乱码

### Python 标准库
- [json.dumps — Python 对象序列化为 JSON 字符串](python/json.dumps/README.md) — `default` / `ensure_ascii` / `indent` 怎么用
- [json.loads — JSON 字符串反序列化为 Python 对象](python/json.loads/README.md) — `object_hook` / `object_pairs_hook` / `parse_float` 实战
- [try-except — Python 异常处理](python/try-except/README.md) — `try/except/else/finally` 四子句 + 异常链 + 自定义异常

### 网络与协议
- [urlparse — URL 解析](网络与协议/01_urlparse-url解析/README.md) — 如何从 URL 字符串中提取 hostname、port 等信息
- [HTTP Headers — Content-Type 与 Authorization](网络与协议/02_http-headers-认证与内容类型/README.md) — 为什么调用 LLM API 必须带上这两个请求头
- [HTTP vs HTTPS — 功能、联系与区别](网络与协议/03_http-vs-https/README.md) — 为什么所有 LLM API 都强制 `https://`
