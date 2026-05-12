#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《别惹女司机》分镜视频播放器
一键生成 + 大窗口播放
"""

from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import subprocess
import json
import os
import threading
import time
from datetime import datetime

app = Flask(__name__)

# 配置
OUTPUT_DIR = Path.home() / "Movies" / "storyboard_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 全局状态
generation_status = {
    "running": False,
    "progress": 0,
    "current_shot": "",
    "message": "就绪",
    "videos": {}
}

# 场景数据
SCENES = {
    "1": {
        "name": "场1：小镇夜",
        "duration": 35,
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
        "duration": 40,
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
        "duration": 90,
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

def check_environment():
    """检查 belt 是否已安装并登录"""
    try:
        # 检查 belt 是否存在
        result = subprocess.run(['which', 'belt'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "未安装 belt CLI，请运行: brew install inference-sh/tap/belt"
        
        # 检查是否登录
        result = subprocess.run(['belt', 'auth', 'status'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return False, "未登录，请运行: belt login"
        
        return True, "环境就绪"
    except Exception as e:
        return False, f"检查失败: {str(e)}"

def generate_single_video(scene_id, shot):
    """生成单个视频"""
    scene_dir = OUTPUT_DIR / f"scene_{scene_id}"
    scene_dir.mkdir(exist_ok=True)
    output_file = scene_dir / f"{shot['name']}.mp4"
    
    if output_file.exists():
        return True, f"{shot['name']} 已存在"
    
    cmd = [
        'belt', 'app', 'run', 'google/veo-3-1-fast',
        '--input', json.dumps({
            "prompt": shot['prompt'],
            "duration": shot['duration'],
            "generate_audio": True
        }),
        '--output', str(output_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            # 尝试从输出中找到生成的文件路径
            # 通常 belt 会输出文件位置
            lines = result.stdout.split('\n')
            for line in lines:
                if '.mp4' in line or 'output' in line.lower():
                    # 如果生成了文件，复制到我们的目录
                    return True, "生成成功"
            return True, "生成成功"
        else:
            return False, f"生成失败: {result.stderr[:200]}"
    except subprocess.TimeoutExpired:
        return False, "生成超时"
    except Exception as e:
        return False, f"异常: {str(e)}"

def generate_all_videos():
    """后台生成所有视频"""
    global generation_status
    
    generation_status["running"] = True
    generation_status["message"] = "正在检查环境..."
    
    # 检查环境
    ok, msg = check_environment()
    if not ok:
        generation_status["running"] = False
        generation_status["message"] = msg
        return
    
    total_shots = sum(len(scene['shots']) for scene in SCENES.values())
    current = 0
    
    for scene_id, scene_data in SCENES.items():
        for shot in scene_data['shots']:
            current += 1
            generation_status["progress"] = int((current / total_shots) * 100)
            generation_status["current_shot"] = f"{shot['name']}: {shot['title']}"
            generation_status["message"] = f"生成中... ({current}/{total_shots})"
            
            success, msg = generate_single_video(scene_id, shot)
            
            if not success:
                generation_status["message"] = f"⚠ {shot['name']} 生成失败: {msg}"
            
            time.sleep(1)  # 避免 API 限流
    
    generation_status["running"] = False
    generation_status["progress"] = 100
    generation_status["message"] = "✓ 全部生成完成！"
    generation_status["videos"] = scan_videos()

def scan_videos():
    """扫描已生成的视频"""
    videos = {}
    for scene_id in SCENES.keys():
        scene_dir = OUTPUT_DIR / f"scene_{scene_id}"
        if scene_dir.exists():
            videos[f"scene_{scene_id}"] = [
                f.name for f in scene_dir.glob("*.mp4")
            ]
    return videos

# 生成锁，防止同时多次请求
generation_lock = threading.Lock()

@app.route('/')
def index():
    return send_from_directory(app.root_path, 'storyboard_preview.html')

@app.route('/api/generate-shot', methods=['POST'])
def generate_shot():
    data = request.get_json() or {}
    scene_id = data.get('scene_id')
    shot_name = data.get('shot_name')

    if not scene_id or not shot_name:
        return jsonify({'success': False, 'message': '参数缺失: scene_id 或 shot_name'}), 400

    try:
        scene = SCENES[str(scene_id)]
    except KeyError:
        return jsonify({'success': False, 'message': '无效的场景 ID'}), 400

    shot = next((item for item in scene['shots'] if item['name'] == shot_name), None)
    if not shot:
        return jsonify({'success': False, 'message': '未找到指定镜头'}), 400

    with generation_lock:
        output_file = OUTPUT_DIR / f"scene_{scene_id}" / f"{shot_name}.mp4"
        if output_file.exists():
            return jsonify({'success': True, 'message': '视频已存在', 'file': f'/video/scene_{scene_id}/{shot_name}.mp4', 'generated': False})

        generation_status['running'] = True
        generation_status['current_shot'] = f"{shot_name}: {shot['title']}"
        generation_status['message'] = f"生成中: {shot_name}"

        success, msg = generate_single_video(scene_id, shot)

        generation_status['running'] = False
        generation_status['current_shot'] = ''
        generation_status['progress'] = 100 if success else generation_status['progress']
        generation_status['message'] = msg if success else f"生成失败: {msg}"

        return jsonify({'success': success, 'message': msg, 'file': f'/video/scene_{scene_id}/{shot_name}.mp4', 'generated': success})

@app.route('/api/status')
def status():
    return jsonify(generation_status)

@app.route('/api/start-generation', methods=['POST'])
def start_generation():
    if generation_status["running"]:
        return jsonify({"success": False, "message": "已有任务在运行"})
    
    thread = threading.Thread(target=generate_all_videos)
    thread.daemon = True
    thread.start()
    
    return jsonify({"success": True, "message": "已开始生成"})

@app.route('/api/videos')
def get_videos():
    return jsonify({
        "videos": scan_videos(),
        "output_dir": str(OUTPUT_DIR)
    })

@app.route('/api/check-env')
def check_env():
    ok, msg = check_environment()
    return jsonify({"ok": ok, "message": msg})

@app.route('/video/<path:filename>')
def serve_video(filename):
    """提供视频文件"""
    video_path = OUTPUT_DIR / filename
    if video_path.exists():
        from flask import send_file
        return send_file(str(video_path), mimetype='video/mp4')
    return "Not found", 404

if __name__ == '__main__':
    print("=" * 60)
    print("《别惹女司机》分镜视频播放器")
    print("=" * 60)
    print(f"输出目录: {OUTPUT_DIR}")
    print("\n正在启动网页服务...")
    print("打开浏览器访问: http://localhost:5000")
    print("\n按 Ctrl+C 停止")
    print("=" * 60)
    
    import webbrowser
    import time
    
    # 延迟打开浏览器，让服务器先启动
    threading.Thread(
        target=lambda: (time.sleep(1), webbrowser.open('http://localhost:5000')),
        daemon=True
    ).start()
    
    app.run(debug=False, host='localhost', port=5000)
