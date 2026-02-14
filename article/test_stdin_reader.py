
import sys

print(f"isatty: {sys.stdin.isatty()}", file=sys.stderr)

line1 = sys.stdin.readline()
print(f"Line1: {repr(line1)}", file=sys.stderr)

line2 = sys.stdin.readline()
print(f"Line2: {repr(line2)}", file=sys.stderr)

try:
    line2.encode('utf-8')
    print("Line2编码正常", file=sys.stderr)
except UnicodeEncodeError as e:
    print(f"Line2编码错误: {e}", file=sys.stderr)
    cleaned = line2.encode('utf-8', errors='ignore').decode('utf-8')
    print(f"清理后: {repr(cleaned)}", file=sys.stderr)

theme = line2.strip()
print(f"主题: {repr(theme)}", file=sys.stderr)
