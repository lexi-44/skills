# 《别惹女司机》分镜视频生成与播放指南

## 🎬 三步快速开始

### 第1步：安装 inference.sh CLI

```bash
# macOS
brew install inference-sh/tap/belt

# 验证安装
belt --version
```

### 第2步：登录 & 获取 API 权限

```bash
belt login
```

按照提示完成登录（需要 inference.sh 账户）

### 第3步：生成视频

```bash
cd /Users/chenlingxuan/Desktop/Work/Artefact/skills

# 运行生成脚本
python3 generate_videos.py
```

脚本会自动生成所有分镜视频，保存到 `~/Movies/storyboard_videos/`

### 第4步：在网页上播放

生成完成后，刷新浏览器或直接打开：
```
/Users/chenlingxuan/Desktop/Work/Artefact/skills/storyboard_preview.html
```

选择场景 → 选择镜头 → 点击"播放选中" → 观看

---

## 📁 文件说明

| 文件 | 用途 |
|------|------|
| `storyboard_preview.html` | 📹 网页播放器 & 分镜预览 |
| `generate_videos.py` | 🎯 视频生成脚本 |
| `storyboard_breakdown_scenes123_chn.csv` | 📊 分镜表（CSV 格式）|
| `generate_video_scenes123_chn.sh` | 🔧 Bash 脚本版本 |

---

## 🎨 输出结构

视频生成后的目录结构：
```
~/Movies/storyboard_videos/
├── scene_1/          # 场 1：小镇夜
│   ├── 1-1.mp4       # 建立环境的空镇全景
│   ├── 1-2-7.mp4     # 雨衣人穿梭与逃离
│   ├── 1-5-6.mp4     # 摩托车威胁与躲避
│   └── 1-7.mp4       # 冲向高速出口
├── scene_2/          # 场 2：高速公路边夜
│   ├── 2-1-2.mp4     # 高围栏的压迫感
│   ├── 2-3-5.mp4     # 两次失败的攀爬
│   └── 2-6-8.mp4     # 意志突破与进入
└── scene_3/          # 场 3：货车服务区黎明前
    ├── 3-1.mp4       # 货车迷宫与潜行
    ├── 3-4-7.mp4     # 司机惊醒与警报
    ├── 3-8-10.mp4    # 夏添登场与职业
    └── 3-11-14.mp4   # 偷上车与转场
```

---

## ⚙️ 生成脚本选项

### 使用 Python 脚本（推荐）

```bash
python3 generate_videos.py
```

自动检测环境，逐个生成视频，显示进度。

### 使用 Bash 脚本

```bash
bash generate_video_scenes123_chn.sh
```

逐场景运行 `belt app run` 命令。

---

## 💡 常见问题

### Q: 视频生成很慢？
**A:** Google Veo 3.1 每个视频需要 30-120 秒，这是正常的。

### Q: 网页打开后看不到视频？
**A:** 
1. 确保已运行生成脚本
2. 检查 `~/Movies/storyboard_videos/` 是否有 mp4 文件
3. 刷新浏览器
4. 如果仍无法检测，手动输入视频路径

### Q: 如何更换 AI 模型？
修改 `generate_videos.py` 中的：
```python
'belt', 'app', 'run', 'google/veo-3-1-fast',  # ← 改这里
```

可选模型：
- `google/veo-3-1` （高质量，慢）
- `falai/seedance-2-t2v` （快速）
- `alibaba/happyhorse-1-0-t2v` （真实感）

### Q: 如何修改视频参数？
编辑 `generate_videos.py` 中的 `SCENES` 字典：
```python
"duration": 5,  # 修改视频时长
"prompt": "..."  # 修改 AI 提示词
```

---

## 🎯 提示词质量建议

所有提示词已按照"中国县城农村生活纪录片 + 温暖真实"风格全中文化。

如需微调，关键词：
- `温暖纪录感 / 低饱和 / 真实纪录片`
- `纪录美学 / 电影质感 / 温暖色调`
- `县城 / 农村 / 真实生活`

---

## 📞 技术支持

- inference.sh 文档：https://docs.inference.sh
- belt CLI 安装：https://github.com/inference-sh/belt
- 本项目 CSV 和 Markdown 参考文件已在同目录

---

**生成完成后，享受你的分镜视频！🎬**
