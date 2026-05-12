#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 一条命令运行所有
"""
import subprocess
import sys
import os
from pathlib import Path

# 进入脚本目录
script_dir = Path(__file__).parent
os.chdir(script_dir)

print("\n" + "="*60)
print("《别惹女司机》分镜视频播放器")
print("="*60)

# 检查并创建必要目录
templates_dir = script_dir / 'templates'
templates_dir.mkdir(exist_ok=True)

# 检查依赖
print("\n检查依赖...")
try:
    import flask
except ImportError:
    print("  → 安装 Flask...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'flask', '-q'], check=True)

print("  ✓ 依赖完整\n")

# 检查 belt 环装
print("检查 belt CLI...")
result = subprocess.run(['which', 'belt'], capture_output=True)
if result.returncode != 0:
    print("  ⚠ 警告: 未安装 belt CLI")
    print("  → 需要运行: brew install inference-sh/tap/belt")
    print("  → 然后运行: belt login\n")
else:
    print("  ✓ belt 已安装\n")

# 运行应用
print("启动网页服务...\n")
subprocess.run([sys.executable, str(script_dir / 'app.py')])
