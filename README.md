# JSON转义工具集

[English Version](README_EN.md)

这个工具集提供了多种方式来处理JSON字符串的转义操作。

## 工具列表

### 1. 命令行版本 (unescape_json.py)
原始的命令行工具，支持文件输入输出。

```bash
python3 unescape_json.py input.txt -n 2 -o out.txt
python3 unescape_json.py input.txt -zh
```

### 2. Web图形界面版本 (web_unescape_json.py)
基于Flask的Web应用，提供现代化的用户界面。

```bash
# 启动Web服务器
source venv/bin/activate
python web_unescape_json.py

# 然后在浏览器中访问 http://127.0.0.1:8080
```

特点：
- 🎨 现代化界面设计
- 🌐 支持中英文双语切换
- 📱 响应式布局，支持移动端
- ⚡ 实时转义处理
- 📋 一键复制结果
- 🔄 Unicode转中文支持
- 🔢 可自定义转义次数

### 3. 交互式命令行版本 (interactive_unescape_json.py)
交互式命令行工具，适合快速处理单个字符串。

```bash
python3 interactive_unescape_json.py
```

特点：
- 💬 交互式操作
- 🔄 支持批量处理
- 📊 实时结果显示
- ✅ JSON格式验证

### 4. GUI桌面版本 (gui_unescape_json.py)
基于tkinter的桌面应用（需要系统支持tkinter）。

```bash
python3 gui_unescape_json.py
```

特点：
- 🖥️ 桌面应用界面
- 📋 剪贴板集成
- 🔄 多轮转义支持
- 💾 状态保持

## 功能特性

所有版本都支持以下核心功能：

1. **智能转义**: 自动检测JSON格式，避免过度转义
2. **Unicode转换**: 支持将Unicode编码转换为中文字符
3. **错误处理**: 完善的异常处理和错误提示
4. **格式验证**: 自动验证结果是否为有效JSON

## 使用示例

### 输入示例
```
{\"name\": \"\\u5f20\\u4e09\", \"age\": 25, \"city\": \"\\u5317\\u4eac\"}
```

### 输出结果
```json
{"name": "张三", "age": 25, "city": "北京"}
```

## 安装要求

- Python 3.6+
- Flask (仅Web版本需要)

### 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装Flask
pip install flask
```

## 快速开始

1. **Web版本**（推荐）:
   ```bash
   source venv/bin/activate
   python web_unescape_json.py
   # 访问 http://127.0.0.1:8080
   ```

2. **交互式版本**:
   ```bash
   python3 interactive_unescape_json.py
   ```

3. **命令行版本**:
   ```bash
   echo '{\"test\": \"\\u4e2d\\u6587\"}' > input.txt
   python3 unescape_json.py input.txt -zh
   ```

## 注意事项

- Web版本默认运行在8080端口
- 所有工具都支持UTF-8编码
- 转义操作会自动检测有效JSON，避免过度处理
- Unicode转换功能可选，按需使用

## 更新日志

- v1.0: 基础转义功能
- v2.0: 增加Web界面和交互式版本
- v2.1: 优化界面设计和用户体验
- v2.2: 新增中英文双语切换功能和转义次数设置