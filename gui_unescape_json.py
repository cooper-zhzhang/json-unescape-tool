#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import re
import json


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


class JSONUnescapeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON转义工具")
        self.root.geometry("800x600")
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap('')
        except:
            pass
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 输入区域
        ttk.Label(main_frame, text="输入内容:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.input_text = scrolledtext.ScrolledText(main_frame, height=15, width=60, wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 选项区域
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        self.convert_unicode_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="转换为中文", variable=self.convert_unicode_var).pack(side=tk.LEFT, padx=(0, 20))
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=1, sticky=tk.E)
        
        ttk.Button(button_frame, text="转义", command=self.unescape_text).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清空", command=self.clear_all).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="复制结果", command=self.copy_result).pack(side=tk.LEFT)
        
        # 输出区域
        ttk.Label(main_frame, text="输出结果:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.output_text = scrolledtext.ScrolledText(main_frame, height=15, width=60, wrap=tk.WORD)
        self.output_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def unescape_text(self):
        """执行转义操作"""
        try:
            input_content = self.input_text.get("1.0", tk.END).strip()
            
            if not input_content:
                messagebox.showwarning("警告", "请输入内容！")
                return
            
            # 执行转义
            result = multi_unescape(input_content)
            
            # 如果需要转换为中文
            if self.convert_unicode_var.get():
                result = unicode_to_chinese_only(result)
            
            # 显示结果
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            
            # 更新状态
            self.status_var.set("转义完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"转义过程中发生错误:\n{str(e)}")
            self.status_var.set("转义失败")
    
    def clear_all(self):
        """清空所有内容"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.status_var.set("已清空")
    
    def copy_result(self):
        """复制结果到剪贴板"""
        try:
            result = self.output_text.get("1.0", tk.END).strip()
            if result:
                self.root.clipboard_clear()
                self.root.clipboard_append(result)
                self.status_var.set("结果已复制到剪贴板")
            else:
                messagebox.showinfo("提示", "没有可复制的内容")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败:\n{str(e)}")


def main():
    """主函数"""
    root = tk.Tk()
    app = JSONUnescapeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()