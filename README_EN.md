# JSON Unescape Tool Collection

This tool collection provides multiple ways to handle JSON string unescaping operations.

## Tool List

### 1. Command Line Version (unescape_json.py)
Original command-line tool supporting file input and output.

```bash
python3 unescape_json.py input.txt -n 2 -o out.txt
python3 unescape_json.py input.txt -zh
```

### 2. Web GUI Version (web_unescape_json.py)
Flask-based web application with modern user interface.

```bash
# Start web server
source venv/bin/activate
python web_unescape_json.py

# Then access http://127.0.0.1:8080 in your browser
```

Features:
- 🎨 Modern interface design
- 🌐 Support for Chinese-English bilingual switching
- 📱 Responsive layout, mobile-friendly
- ⚡ Real-time unescape processing
- 📋 One-click result copying
- 🔄 Unicode to Chinese conversion support
- 🔢 Customizable number of unescape iterations

### 3. Interactive Command Line Version (interactive_unescape_json.py)
Interactive command-line tool, suitable for quick processing of single strings.

```bash
python3 interactive_unescape_json.py
```

Features:
- 💬 Interactive operation
- 🔄 Support for batch processing
- 📊 Real-time result display
- ✅ JSON format validation

### 4. GUI Desktop Version (gui_unescape_json.py)
Desktop application based on tkinter (requires system tkinter support).

```bash
python3 gui_unescape_json.py
```

Features:
- 🖥️ Desktop application interface
- 📋 Clipboard integration
- 🔄 Multi-round unescape support
- 💾 State persistence

## Features

All versions support the following core features:

1. **Smart Unescape**: Automatically detects JSON format to avoid over-processing
2. **Unicode Conversion**: Supports converting Unicode encoding to Chinese characters
3. **Error Handling**: Comprehensive exception handling and error prompts
4. **Format Validation**: Automatically validates if the result is valid JSON

## Usage Examples

### Input Example
```
{\"name\": \"\\u5f20\\u4e09\", \"age\": 25, \"city\": \"\\u5317\\u4eac\"}
```

### Output Result
```json
{"name": "张三", "age": 25, "city": "北京"}
```

## Installation Requirements

- Python 3.6+
- Flask (Web version only)

### Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install Flask
pip install flask
```

## Quick Start

1. **Web Version** (Recommended):
   ```bash
   source venv/bin/activate
   python web_unescape_json.py
   # Access http://127.0.0.1:8080
   ```

2. **Interactive Version**:
   ```bash
   python3 interactive_unescape_json.py
   ```

3. **Command Line Version**:
   ```bash
   echo '{\"test\": \"\\u4e2d\\u6587\"}' > input.txt
   python3 unescape_json.py input.txt -zh
   ```

## Notes

- Web version runs on port 8080 by default
- All tools support UTF-8 encoding
- Unescape operations automatically detect valid JSON to avoid over-processing
- Unicode conversion feature is optional, use as needed

## Changelog

- v1.0: Basic unescape functionality
- v2.0: Added web interface and interactive version
- v2.1: Optimized interface design and user experience
- v2.2: Added Chinese-English bilingual switching and unescape iteration settings