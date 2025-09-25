#!/usr/bin/env python3

import sys
import re
import json
import os


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


def main():
    """交互式主函数"""
    print("=" * 60)
    print("JSON转义工具 - 交互式版本")
    print("=" * 60)
    print("功能说明：")
    print("1. 自动检测并转义JSON字符串")
    print("2. 支持Unicode转中文")
    print("3. 输入 'quit' 或 'exit' 退出程序")
    print("4. 输入 'clear' 清空屏幕")
    print("=" * 60)
    
    while True:
        try:
            # 获取用户输入
            print("\n请输入要转义的JSON字符串：")
            user_input = input("> ").strip()
            
            # 处理特殊命令
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("感谢使用，再见！")
                break
            elif user_input.lower() == 'clear':
                os.system('clear' if os.name == 'posix' else 'cls')
                continue
            elif not user_input:
                print("请输入内容！")
                continue
            
            # 询问转义次数
            print("转义次数？(0-10，0或留空表示自动检测，默认0): ", end="")
            times_input = input().strip()
            escape_times = None
            if times_input and times_input != '0':
                try:
                    escape_times = int(times_input)
                    if escape_times < 1 or escape_times > 10:
                        print("转义次数必须在1-10之间，使用自动检测")
                        escape_times = None
                except ValueError:
                    print("输入无效，使用自动检测")
                    escape_times = None
            
            # 询问是否转换为中文
            print("是否转换为中文？(y/n，默认n): ", end="")
            convert_choice = input().strip().lower()
            convert_unicode = convert_choice in ['y', 'yes', '是']
            
            print("\n处理中...")
            
            # 执行转义
            result = multi_unescape(user_input, escape_times)
            
            # 如果需要转换为中文
            if convert_unicode:
                result = unicode_to_chinese_only(result)
            
            # 显示结果
            print("\n" + "=" * 40)
            print("转义结果：")
            print("=" * 40)
            print(result)
            print("=" * 40)
            
            # 检查结果是否为有效JSON
            if is_valid_json(result):
                print("✓ 结果为有效的JSON格式")
            else:
                print("⚠ 结果可能不是有效的JSON格式")
            
            # 询问是否继续
            print("\n是否继续？(y/n，默认y): ", end="")
            continue_choice = input().strip().lower()
            if continue_choice in ['n', 'no', '否']:
                print("感谢使用，再见！")
                break
                
        except KeyboardInterrupt:
            print("\n\n程序被中断，再见！")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")
            print("请重试或输入 'quit' 退出")


if __name__ == "__main__":
    main()