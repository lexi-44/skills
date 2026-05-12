#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《别惹女司机》前三场视频生成工具
使用 inference.sh CLI 和 Google Veo 生成分镜头视频
"""

import subprocess
import json
import os
from pathlib import Path
import time

# 输出目录
OUTPUT_DIR = Path.home() / "Movies" / "storyboard_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 场景数据
SCENES = {
    "1": {
        "name": "场1：小镇夜",
        "shots": [
            {
                "name": "1-1",
                "title": "建立环境的空镇全景",
                "duration": 5,
                "prompt": "中国县城空镇街道，午夜暴雨倾泻，湿漉漉的马路反射路灯光线，冷蓝色调笼罩，无人迹象，远处模糊的高速公路服务区灯光隐隐约约，低饱和温暖纪录片美学，电影质感，16:9"
            },
            {
                "name": "1-2-7",
                "title": "雨衣人穿梭与逃离",
                "duration": 12,
                "prompt": "穿着硕大暗色雨衣的人物在暴雨县城街道上匆匆行走，脸完全被帽子遮挡，只见轮廓被路灯背光勾边，积水反射灯光，人物身影渺小孤独，紧张的逃离感，温暖低饱和纪录风格，16:9"
            },
            {
                "name": "1-5-6",
                "title": "摩托车威胁与躲避巷子",
                "duration": 9,
                "prompt": "暴雨中摩托车强光掠过，雨衣人物急速躲进黑色小巷，身体紧贴巷壁，水流从巷口冲入，远处摩托声渐远，紧张悬疑氛围，纪录片真实感，16:9"
            },
            {
                "name": "1-7",
                "title": "冲向高速出口的小身影",
                "duration": 6,
                "prompt": "暴雨中小人物从县城街道冲向远处的高速公路服务区亮光，身影在雨幕中显得渺小坚定，黎明前的蓝色调与远处灯光混合，推进感强烈，温暖纪录美学，16:9"
            }
        ]
    },
    "2": {
        "name": "场2：高速公路边夜",
        "shots": [
            {
                "name": "2-1-2",
                "title": "高围栏的压迫感",
                "duration": 9,
                "prompt": "高速公路边的高围栏正对镜头竖立，冷硬的铁网占据2/3画面，栏杆形成压迫线条，人物在底部显得极其渺小，脚踩泥地积水，远处服务区隐约灯光，寒冷压抑，纪录片风格，16:9"
            },
            {
                "name": "2-3-5",
                "title": "两次失败的攀爬",
                "duration": 17,
                "prompt": "雨衣人物第一次攀爬高围栏，手抓铁网，肌肉绷紧，突然失力摔下，身体坠入泥地溅起水花，沾满泥污，喘息声沉重，人物咬牙再次站起，再度尝试，这次更狼狈，绝望与坚持交织，温暖纪录感，16:9"
            },
            {
                "name": "2-6-8",
                "title": "意志突破与进入服务区",
                "duration": 13,
                "prompt": "特写雨水混合泪水顺脸线流下，紧咬的嘴角，眼神坚定的瞬间，停顿凝重，随后人物最终翻过高围栏顶部，剪影中身体背后是服务区灯光，走向前方的灯光与黎明天光混合区域，跛足但坚持，纪录片风格，16:9"
            }
        ]
    },
    "3": {
        "name": "场3：货车服务区黎明前",
        "shots": [
            {
                "name": "3-1",
                "title": "货车迷宫与潜行",
                "duration": 15,
                "prompt": "从高位俯视，密集的大货车排成阵列如钢铁迷宫，车窗全被帘子遮挡，黎明前的冷蓝色调，雨雾笼罩。低角度跟拍：大货车轮胎和底盘占据画面，雨衣人身影渺小地在车缝间踮脚移动。特写：雨衣手臂伸向货车门，门锁发出金属轻响，失败的瞬间，纪录感，16:9"
            },
            {
                "name": "3-4-7",
                "title": "司机惊醒与警报扩散",
                "duration": 20,
                "prompt": "透过货车窗缝帘子，司机被惊醒的模糊人影，张师傅下车咒骂。极低角度拍摄：大货车底盘黑暗横跨画面，雨衣人身体贴地钻入暗处。多窗格构图：周围几辆货车窗户依次亮起，帘子晃动，多个司机轮廓从睡眠中惊起，方言咒骂声，危险感扩大，纪录感，16:9"
            },
            {
                "name": "3-8-10",
                "title": "夏添登场与职业细节",
                "duration": 20,
                "prompt": "蓬乱鸡窝头的中年货车司机夏添从车窗探出，睡衣样穿着，形成与周围紧张氛围的喜感反差。两个司机在密集货车间方言对话，展现老司机的日常烟火气。快速蒙太奇：特写油箱检查、封条完好、轮胎气压测试、用铁棍绞缠固定绳、拍打车头检查，每个动作展现职业素养，纪录感，16:9"
            },
            {
                "name": "3-11-14",
                "title": "雨衣人偷上车与转场",
                "duration": 18,
                "prompt": "夏添在后厢检查被前景遮挡，同时雨衣人从阴影中钻出靠近驾驶室车门。车门打开形成暗框，雨衣人身体迅速钻入驾驶室，动作干脆利落。夏添从外面走向驾驶室爬上车，发动机声响起。货车从服务区停放位驶出朝向高速方向，车灯切开雨幕，黎明天光与夜色混合，纪录感，16:9"
            }
        ]
    }
}

def check_belt_installed():
    """检查 belt CLI 是否已安装"""
    try:
        result = subprocess.run(['which', 'belt'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ belt CLI 已安装")
            return True
        else:
            print("✗ 未找到 belt CLI")
            print("  请先运行: brew install inference-sh/tap/belt")
            return False
    except Exception as e:
        print(f"✗ 检查失败: {e}")
        return False

def generate_video(scene_id, shot_name, prompt, duration, output_path):
    """调用 belt 生成单个视频"""
    cmd = [
        'belt', 'app', 'run', 'google/veo-3-1-fast',
        '--input', json.dumps({
            "prompt": prompt,
            "duration": duration,
            "generate_audio": True
        }),
        '--output', str(output_path)
    ]
    
    try:
        print(f"  生成中: {shot_name} ({duration}s)...", end=" ", flush=True)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✓")
            return True
        else:
            print(f"✗\n    错误: {result.stderr[:100]}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ (超时)")
        return False
    except Exception as e:
        print(f"✗\n    异常: {e}")
        return False

def main():
    print("=" * 60)
    print("《别惹女司机》分镜视频生成工具")
    print("=" * 60)
    print(f"输出目录: {OUTPUT_DIR}\n")
    
    # 检查环境
    if not check_belt_installed():
        print("\n需要先安装 inference.sh CLI")
        print("  macOS: brew install inference-sh/tap/belt")
        print("  然后运行: belt login")
        return
    
    # 检查登录状态
    try:
        result = subprocess.run(['belt', 'auth', 'status'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("\n✗ 需要登录")
            print("  请运行: belt login")
            return
        else:
            print("✓ 已登录\n")
    except:
        pass
    
    # 生成视频
    total_videos = 0
    successful = 0
    
    for scene_id, scene_data in SCENES.items():
        print(f"[场景 {scene_id}] {scene_data['name']}")
        
        scene_dir = OUTPUT_DIR / f"scene_{scene_id}"
        scene_dir.mkdir(exist_ok=True)
        
        for shot in scene_data['shots']:
            output_file = scene_dir / f"{shot['name']}.mp4"
            total_videos += 1
            
            if output_file.exists():
                print(f"  ✓ {shot['name']} (已存在)")
                successful += 1
            else:
                if generate_video(scene_id, shot['name'], shot['prompt'], shot['duration'], output_file):
                    successful += 1
                time.sleep(1)  # 避免API限流
        
        print()
    
    print("=" * 60)
    print(f"完成: {successful}/{total_videos} 个视频")
    print(f"位置: {OUTPUT_DIR}")
    print("=" * 60)
    
    if successful > 0:
        print("\n下一步: 用浏览器打开 storyboard_preview.html")
        print("        网页会自动显示已生成的视频")

if __name__ == '__main__':
    main()
