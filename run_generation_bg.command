#!/usr/bin/env bash
cd "$(dirname "$0")"

# 后台运行视频生成，不打印到终端
if ! command -v belt >/dev/null 2>&1; then
  echo "未检测到 belt CLI，请先安装：brew install inference-sh/tap/belt"
  exit 1
fi

if ! belt auth status >/dev/null 2>&1; then
  echo "未检测到 belt 登录，请先运行：belt login"
  exit 1
fi

nohup python3 generate_videos.py > generate_videos.log 2>&1 &
PID=$!
echo "已在后台启动生成任务，PID=$PID"
echo "日志文件：$(pwd)/generate_videos.log"
echo "输出目录：$HOME/Movies/storyboard_videos"
