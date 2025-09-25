#!/usr/bin/env python3

import sys
import re
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)


def is_valid_json(s):
    """检查字符串是否为有效的JSON格式"""
    try:
        json.loads(s)
        return True
    except Exception:
        return False


def multi_unescape(s, times=None):
    """多次unescape字符串，支持自动检测合法JSON"""
    if is_valid_json(s):
        return s
    if times is None:
        temp = s
        for i in range(10):
            try:
                s_new = bytes(s, "utf-8").decode("unicode_escape")
            except Exception as e:
                print(f"Exception occurred at unescape #{i+1}: {e}, stop converting.", file=sys.stderr)
                break
            if '\\x' in s_new:
                print(f"Found \\x escape after unescape #{i+1}, stop converting.", file=sys.stderr)
                break
            s = s_new
            if is_valid_json(s):
                return s
        return temp
    else:
        for i in range(times):
            try:
                s_new = bytes(s, "utf-8").decode("unicode_escape")
            except Exception as e:
                print(f"Exception occurred at unescape #{i+1}: {e}, stop converting.", file=sys.stderr)
                break
            s = s_new
        return s


def unicode_to_chinese_only(s):
    """将Unicode编码转换为中文字符"""
    def repl(match):
        return chr(int(match.group(1), 16))
    return re.sub(r'\\u([0-9a-fA-F]{4})', repl, s)


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/unescape', methods=['POST'])
def unescape():
    """处理转义请求"""
    try:
        data = request.get_json()
        input_text = data.get('text', '')
        convert_unicode = data.get('convert_unicode', False)
        escape_times = data.get('escape_times', None)
        
        if not input_text.strip():
            return jsonify({
                'success': False,
                'error': '请输入内容'
            })
        
        # 处理转义次数参数
        if escape_times is not None:
            if escape_times == 0:
                escape_times = None  # 0表示不设置转义次数
            else:
                escape_times = int(escape_times)
        
        # 执行转义
        result = multi_unescape(input_text, escape_times)
        
        # 如果需要转换为中文
        if convert_unicode:
            result = unicode_to_chinese_only(result)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/static/<path:filename>')
def static_files(filename):
    """提供静态文件服务"""
    return send_from_directory('content', filename)


if __name__ == '__main__':
    # 创建templates目录和HTML文件
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 创建HTML模板
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON转义工具</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 25px;
        }
        
        .section h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        textarea {
            width: 100%;
            min-height: 200px;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
            transition: border-color 0.3s ease;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .checkbox-group input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: #667eea;
        }
        
        .checkbox-group label {
            color: #555;
            font-weight: 500;
            cursor: pointer;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #f8f9fa;
            color: #495057;
            border: 2px solid #e9ecef;
        }
        
        .btn-secondary:hover {
            background: #e9ecef;
            transform: translateY(-1px);
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-success:hover {
            background: #218838;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        }
        
        .status {
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
            font-weight: 500;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .example {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin-bottom: 20px;
        }
        
        .example h4 {
            color: #495057;
            margin-bottom: 8px;
        }
        
        .example code {
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 13px;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 8px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .content {
                padding: 20px;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .button-group {
                justify-content: center;
            }
            
            textarea {
                min-height: 150px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 id="pageTitle">JSON转义工具</h1>
                    <p id="pageSubtitle">智能JSON字符串转义与Unicode转换工具</p>
                </div>
                <div>
                    <button id="langZh" onclick="switchLanguage('zh')" style="margin-right: 10px; padding: 8px 16px; background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); border-radius: 5px; cursor: pointer; font-weight: bold;">中文</button>
                    <button id="langEn" onclick="switchLanguage('en')" style="padding: 8px 16px; background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); border-radius: 5px; cursor: pointer;">English</button>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="example">
                <h4 id="exampleTitle">使用示例：</h4>
                <div id="exampleInput">
                    <img src="/content/image.png" alt="示例输入" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px;">
                </div>
                <p id="exampleOutput">输出：<code>{"name": "张三", "age": 25, "city": "北京"}</code></p>
            </div>
            
            <div class="section">
                <h3 id="inputTitle">输入内容：</h3>
                <textarea id="inputText" placeholder="请输入需要转义的JSON字符串..."></textarea>
            </div>
            
            <div class="controls">
                <div class="checkbox-group">
                    <input type="checkbox" id="convertUnicode" checked>
                    <label for="convertUnicode" id="convertLabel">转换为中文</label>
                </div>
                
                <div class="button-group">
                    <button class="btn-primary" onclick="unescapeText()">
                        <span>🔄</span>
                        <span id="btnConvert">开始转义</span>
                    </button>
                    <button class="btn-secondary" onclick="clearAll()">
                        <span>🗑️</span>
                        <span id="btnClear">清空</span>
                    </button>
                    <button class="btn-success" onclick="copyResult()">
                        <span>📋</span>
                        <span id="btnCopy">复制结果</span>
                    </button>
                </div>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p id="loadingText">正在处理中...</p>
            </div>
            
            <div class="status" id="status"></div>
            
            <div class="section">
                <h3 id="outputTitle">输出结果：</h3>
                <textarea id="outputText" placeholder="转义后的结果将显示在这里..." readonly></textarea>
            </div>
        </div>
    </div>

    <script>
        // 语言翻译对象
        const translations = {
            zh: {
                pageTitle: 'JSON转义工具',
                pageSubtitle: '智能JSON字符串转义与Unicode转换工具',
                exampleTitle: '使用示例：',
                exampleInput: '输入: <code>{\\\\"name\\\\": \\\\"\\\\\\\\u5f20\\\\\\\\u4e09", \\\\"age\\\\": 25, \\\\"city\\\\": \\\\"\\\\\\\\u5317\\\\\\\\u4eac\\\\"}</code><br><small>Note: \\\\u represents Unicode escape sequence</small>',
                exampleOutput: '输出：<code>{"name": "张三", "age": 25, "city": "北京"}</code>',
                inputTitle: '输入内容：',
                inputPlaceholder: '请输入需要转义的JSON字符串...',
                convertLabel: '转换Unicode编码',
                btnConvert: '开始转义',
                btnClear: '清空',
                btnCopy: '复制结果',
                loadingText: '正在处理中...',
                outputTitle: '输出结果：',
                outputPlaceholder: '转义后的结果将显示在这里...',
                statusNoContent: '请输入内容',
                statusCopySuccess: '复制成功！',
                statusCopyError: '复制失败，请手动复制'
            },
            en: {
                pageTitle: 'JSON Unescape Tool',
                pageSubtitle: 'Smart JSON String Unescape and Unicode Conversion Tool',
                exampleTitle: 'Usage Example:',
                exampleInput: 'Input: <code>{\\\\"name\\\\": \\\\"\\\\\\\\u5f20\\\\\\\\u4e09", \\\\"age\\\\": 25, \\\\"city\\\\": \\\\"\\\\\\\\u5317\\\\\\\\u4eac\\\\"}</code><br><small>Note: \\\\u represents Unicode escape sequence</small>',
                exampleOutput: 'Output: <code>{"name": "张三", "age": 25, "city": "北京"}</code>',
                inputTitle: 'Input Content:',
                inputPlaceholder: 'Please enter JSON string to unescape...',
                convertLabel: 'Convert Unicode Encoding',
                btnConvert: 'Start Unescape',
                btnClear: 'Clear',
                btnCopy: 'Copy Result',
                loadingText: 'Processing...',
                outputTitle: 'Output Result:',
                outputPlaceholder: 'Unescaped result will be displayed here...',
                statusNoContent: 'Please enter content',
                statusCopySuccess: 'Copy successful!',
                statusCopyError: 'Copy failed, please copy manually'
            }
        };
        
        // 当前语言
        let currentLang = 'zh';
        
        // 切换语言函数
        function switchLanguage(lang) {
            currentLang = lang;
            const t = translations[lang];
            
            // 更新页面标题和副标题
            document.getElementById('pageTitle').textContent = t.pageTitle;
            document.getElementById('pageSubtitle').textContent = t.pageSubtitle;
            
            // 更新示例部分
            document.getElementById('exampleTitle').textContent = t.exampleTitle;
            document.getElementById('exampleInput').innerHTML = t.exampleInput;
            document.getElementById('exampleOutput').innerHTML = t.exampleOutput;
            
            // 更新输入输出部分
            document.getElementById('inputTitle').textContent = t.inputTitle;
            document.getElementById('inputText').placeholder = t.inputPlaceholder;
            document.getElementById('convertLabel').textContent = t.convertLabel;
            document.getElementById('btnConvert').textContent = t.btnConvert;
            document.getElementById('btnClear').textContent = t.btnClear;
            document.getElementById('btnCopy').textContent = t.btnCopy;
            document.getElementById('loadingText').textContent = t.loadingText;
            document.getElementById('outputTitle').textContent = t.outputTitle;
            document.getElementById('outputText').placeholder = t.outputPlaceholder;
            
            // 更新语言按钮样式
            document.getElementById('langZh').style.fontWeight = lang === 'zh' ? 'bold' : 'normal';
            document.getElementById('langEn').style.fontWeight = lang === 'en' ? 'bold' : 'normal';
        }
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            switchLanguage('zh');
        });
        async function unescapeText() {
            const inputText = document.getElementById('inputText').value.trim();
            const convertUnicode = document.getElementById('convertUnicode').checked;
            const outputText = document.getElementById('outputText');
            const status = document.getElementById('status');
            const loading = document.getElementById('loading');
            
            if (!inputText) {
                showStatus('请输入内容！', 'error');
                return;
            }
            
            // 显示加载状态
            loading.style.display = 'block';
            status.style.display = 'none';
            
            try {
                const response = await fetch('/unescape', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: inputText,
                        convert_unicode: convertUnicode
                    })
                });
                
                const data = await response.json();
                
                loading.style.display = 'none';
                
                if (data.success) {
                    outputText.value = data.result;
                    showStatus('转义成功！', 'success');
                } else {
                    showStatus('转义失败：' + data.error, 'error');
                }
            } catch (error) {
                loading.style.display = 'none';
                showStatus('网络错误：' + error.message, 'error');
            }
        }
        
        function clearAll() {
            document.getElementById('inputText').value = '';
            document.getElementById('outputText').value = '';
            document.getElementById('status').style.display = 'none';
        }
        
        function copyResult() {
            const outputText = document.getElementById('outputText').value;
            if (!outputText) {
                showStatus(translations[currentLang].statusNoContent, 'error');
                return;
            }
            
            // 使用现代剪贴板API
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(outputText).then(function() {
                    showStatus(translations[currentLang].statusCopySuccess, 'success');
                }).catch(function(err) {
                    console.error('复制失败:', err);
                    fallbackCopy(outputText);
                });
            } else {
                // 降级方案
                fallbackCopy(outputText);
            }
        }
        
        // 降级复制方案
        function fallbackCopy(text) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                showStatus(translations[currentLang].statusCopySuccess, 'success');
            } catch (err) {
                console.error('复制失败:', err);
                showStatus(translations[currentLang].statusCopyError, 'error');
            } finally {
                document.body.removeChild(textArea);
            }
        }
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
            
            // 3秒后自动隐藏状态信息
            setTimeout(() => {
                status.style.display = 'none';
            }, 3000);
        }
        
        // 支持Ctrl+Enter快捷键
        document.getElementById('inputText').addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                unescapeText();
            }
        });
    </script>
</body>
</html>'''
    
    # 写入HTML文件
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Web界面已创建完成！")
    print("正在启动Flask服务器...")
    
    # 启动Flask应用
    app.run(debug=True, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()