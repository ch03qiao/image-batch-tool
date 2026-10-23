# 🖼 图片批量处理工具（压缩·改尺寸·加水印）

> 人工智专业在校接单作品 · 电商主图、头像、素材图一键批量处理。
> 支持命令行与图形界面两种用法。

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/powered%20by-Pillow-3776AB)

---

## ✨ 功能

- 📉 **批量压缩**：按最长边缩放到指定尺寸（如 1080px），体积立减 70%+
- 💧 **批量水印**：右下角加文字水印，防盗用
- 🔄 **格式互转**：JPG / PNG / WEBP 任意互转
- 🖥 **带 GUI**：图形界面选文件夹即可，无需命令行

---

## 🚀 快速开始

```bash
pip install -r requirements.txt

# 命令行
python 示例2_图片批量处理.py 原图文件夹 -o 成品文件夹 --max-size 1080 --quality 80 --watermark "你的店名"

# 或直接双击运行（图形界面）
python 示例2_图片批量处理.py
```

### 参数说明
| 参数 | 默认值 | 说明 |
|---|---|---|
| `--max-size` | 1080 | 缩放后最长边像素 |
| `--quality` | 80 | JPEG 压缩质量(1–100) |
| `--watermark` | 无 | 水印文字，留空不加 |

---

## 📸 效果演示

**输入**：3 张 1536×1024 高清图（单张 2–4 MB）
**输出**：3 张 ≤1080px + 右下角水印，单张约 200–400 KB，画质肉眼无损。

---

## 💼 接单场景

- 淘宝/拼多多/抖音店铺主图批量压缩加水印
- 活动海报导出多尺寸
- 头像/写真批量转格式

📩 接单联系见 [个人主页](https://github.com/ch03qiao)。
