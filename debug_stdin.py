# -*- coding: utf-8 -*-
"""
调试stdin读取
"""
import sys

print(f"isatty: {sys.stdin.isatty()}", file=sys.stderr)

if not sys.stdin.isatty():
    line1 = sys.stdin.readline()
    print(f"Line 1: '{line1}' (len={len(line1)})", file=sys.stderr)
    print(f"Line 1 stripped: '{line1.strip()}'", file=sys.stderr)

    line2 = sys.stdin.readline()
    print(f"Line 2: '{line2}' (len={len(line2)})", file=sys.stderr)
    print(f"Line 2 stripped: '{line2.strip()}'", file=sys.stderr)

    line3 = sys.stdin.readline()
    print(f"Line 3: '{line3}' (len={len(line3)})", file=sys.stderr)
    print(f"Line 3 stripped: '{line3.strip()}'", file=sys.stderr)

    sys.exit(0)
else:
    print("No stdin input", file=sys.stderr)
    sys.exit(1)
