#!/usr/bin/env python3

import sys
import argparse
import re
import json


def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except Exception:
        return False

def multi_unescape(s, times=None):
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
    def repl(match):
        return chr(int(match.group(1), 16))
    return re.sub(r'\\u([0-9a-fA-F]{4})', repl, s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="多次 unescape json 字符串（支持自动检测合法json）\n"
                    "Unescape json string multiple times (auto stop if valid json detected)",
        epilog="示例 Example:\n"
               "  python3 unescape_json.py input.txt -n 2 -o out.txt\n"
               "  python3 unescape_json.py input.txt -zh",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('input', nargs='?', help='输入文件名 (Input file name)')
    parser.add_argument('-i', '--input_opt', help='输入文件名 (Input file name, 可选参数名)')
    parser.add_argument('-n', '--number', type=int,
                        help='unescape 次数（可选，不指定则自动最多10次，遇到合法json即停止）\n'
                             'Number of unescape (optional, default: auto up to 10, stop if valid json)')
    parser.add_argument('-o', '--output',
                        help='输出文件名（可选）(Output file name, optional)')
    parser.add_argument('-zh', action='store_true',
                        help='unescape 后再进行 unicode 转中文 (Convert unicode to Chinese after unescape)')
    args = parser.parse_args()

    # 兼容 -i 和位置参数
    input_file = args.input_opt if args.input_opt else args.input
    if not input_file:
        parser.error("必须指定输入文件名（位置参数或 -i）\nInput file name is required (positional or -i)")

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if args.number is not None:
        result = multi_unescape(content, args.number)
    else:
        result = multi_unescape(content, None)

    if args.zh:
        result = unicode_to_chinese_only(result)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
    else:
        print(result)
