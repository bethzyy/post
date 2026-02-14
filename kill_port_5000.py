#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
强制关闭端口5000上的所有进程
"""
import subprocess
import re

def kill_processes_on_port(port):
    """关闭占用指定端口的进程"""
    # 获取占用端口的进程列表
    result = subprocess.run(
        ['netstat', '-ano'],
        capture_output=True,
        text=True,
        encoding='gbk',
        errors='ignore'
    )

    killed_pids = set()

    for line in result.stdout.split('\n'):
        if f':{port}' in line and 'LISTENING' in line:
            # 解析PID
            parts = line.split()
            if len(parts) >= 5:
                pid = parts[-1].strip()
                if pid.isdigit() and pid not in killed_pids:
                    try:
                        print(f"正在终止进程: PID={pid}")
                        subprocess.run(
                            ['taskkill', '/F', '/PID', pid],
                            capture_output=True,
                            encoding='gbk',
                            errors='ignore'
                        )
                        killed_pids.add(pid)
                    except Exception as e:
                        print(f"无法终止进程 {pid}: {e}")

    return len(killed_pids)

if __name__ == '__main__':
    print("=" * 60)
    print("   关闭端口5000上的所有进程")
    print("=" * 60)
    print()

    count = kill_processes_on_port(5000)

    print()
    print(f"已终止 {count} 个进程")
    print("端口5000现在应该是空闲的")
