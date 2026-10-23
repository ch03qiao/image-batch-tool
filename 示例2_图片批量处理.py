# -*- coding: utf-8 -*-
"""
示例2：图片批量处理工具（压缩 / 改尺寸 / 格式转换 / 加水印）
===========================================================
适用场景（电商、自媒体、写真客户的刚需）：
  - 几百张产品图要统一压缩到某个大小，方便上传；
  - 竖图统一改成 1080x1920 发抖音/小红书；
  - JPG 批量转 PNG，或反过来；
  - 给一组图加半透明文字水印防盗用。

为什么选它当示例：
  - 难度低：核心是 Pillow 库的 resize / save / ImageDraw；
  - 卖相好：带图形界面，不懂代码的人也能用 → 适合当"数字产品"在闲鱼卖；
  - 复用率高：几乎每个做内容的客户都要，复购和转介绍多。

用法：
  # 命令行
  python 示例2_图片批量处理.py "D:/原图" -o "D:/成品" --max-size 1080 --quality 80
  python 示例2_图片批量处理.py "D:/原图" -o "D:/成品" --fmt png --watermark "©我的店"

  # 图形界面（给客户用）
  python 示例2_图片批量处理.py --gui
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont


def add_watermark(img, text):
    """在右下角加半透明文字水印。"""
    if not text:
        return img
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", max(18, int(img.width / 25)))
    except Exception:
        font = ImageFont.load_default()
    # 估算文字尺寸
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = img.width - tw - 15
    y = img.height - th - 15
    # 半透明白字 + 阴影，保证各种底色都看得清
    draw.text((x + 1, y + 1), text, font=font, fill=(0, 0, 0, 120))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))
    return img


def process_images(folder, output, max_size=None, quality=80, fmt=None,
                   watermark=None, recursive=False):
    """批量处理一个文件夹里的图片。"""
    os.makedirs(output, exist_ok=True)
    patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"]
    files = []
    for pat in patterns:
        files += glob_collect(folder, pat, recursive)
    files = sorted(set(files))

    if not files:
        print("⚠️ 没找到任何图片文件，请检查路径。")
        return 0

    count = 0
    for f in files:
        try:
            img = Image.open(f).convert("RGB")
        except Exception as e:
            print(f"⚠️ 跳过 {f}：{e}")
            continue

        # 改尺寸：等比缩放到最长边不超过 max_size
        if max_size:
            w, h = img.size
            scale = min(1.0, max_size / max(w, h))
            if scale < 1.0:
                img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

        img = add_watermark(img, watermark)

        # 决定输出格式与扩展名
        out_fmt = (fmt or os.path.splitext(f)[1].lstrip(".")).upper()
        if out_fmt == "JPG":
            out_fmt = "JPEG"
        ext = out_fmt.lower() if out_fmt != "JPEG" else "jpg"
        base = os.path.splitext(os.path.basename(f))[0]
        dst = os.path.join(output, f"{base}.{ext}")

        save_kwargs = {}
        if out_fmt in ("JPEG",):
            save_kwargs["quality"] = quality
        try:
            img.save(dst, out_fmt, **save_kwargs)
            count += 1
        except Exception as e:
            print(f"⚠️ 保存失败 {dst}：{e}")

    print(f"✅ 已处理 {count} 张图片，输出到：{output}")
    return count


def glob_collect(folder, pat, recursive):
    import glob
    return glob.glob(os.path.join(folder, pat if not recursive else os.path.join("**", pat)),
                     recursive=recursive)


def launch_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.title("图片批量处理工具")
    root.geometry("560x360")

    folder_var = tk.StringVar()
    out_var = tk.StringVar(value="成品图")
    size_var = tk.StringVar(value="1080")
    quality_var = tk.StringVar(value="80")
    fmt_var = tk.StringVar(value="保持原格式")
    wm_var = tk.StringVar()
    rec_var = tk.BooleanVar(value=False)

    def pick_folder():
        p = filedialog.askdirectory(title="选择原图文件夹")
        if p:
            folder_var.set(p)

    def pick_out():
        p = filedialog.askdirectory(title="选择输出文件夹")
        if p:
            out_var.set(p)

    def run():
        if not folder_var.get():
            messagebox.showwarning("提示", "请先选择原图文件夹")
            return
        ms = int(size_var.get()) if size_var.get().isdigit() else None
        q = int(quality_var.get()) if quality_var.get().isdigit() else 80
        fmt = None if fmt_var.get() == "保持原格式" else fmt_var.get().lower()
        process_images(folder_var.get(), out_var.get(), max_size=ms, quality=q,
                       fmt=fmt, watermark=wm_var.get() or None, recursive=rec_var.get())
        messagebox.showinfo("完成", "图片已全部处理完")

    tk.Label(root, text="① 原图文件夹：").pack(anchor="w", padx=15, pady=(15, 0))
    f1 = tk.Frame(root); f1.pack(fill="x", padx=15)
    tk.Entry(f1, textvariable=folder_var, width=45).pack(side="left")
    tk.Button(f1, text="浏览", command=pick_folder).pack(side="left", padx=5)

    tk.Label(root, text="② 输出文件夹：").pack(anchor="w", padx=15, pady=(10, 0))
    f2 = tk.Frame(root); f2.pack(fill="x", padx=15)
    tk.Entry(f2, textvariable=out_var, width=45).pack(side="left")
    tk.Button(f2, text="浏览", command=pick_out).pack(side="left", padx=5)

    f3 = tk.Frame(root); f3.pack(fill="x", padx=15, pady=10)
    tk.Label(f3, text="最长边(px)：").pack(side="left")
    tk.Entry(f3, textvariable=size_var, width=8).pack(side="left", padx=3)
    tk.Label(f3, text="质量(1-100)：").pack(side="left", padx=(10, 0))
    tk.Entry(f3, textvariable=quality_var, width=8).pack(side="left", padx=3)
    tk.Label(f3, text="格式：").pack(side="left", padx=(10, 0))
    ttk.Combobox(f3, textvariable=fmt_var, width=12,
                 values=["保持原格式", "jpg", "png", "webp"]).pack(side="left")

    tk.Label(root, text="水印文字（留空不加）：").pack(anchor="w", padx=15)
    tk.Entry(root, textvariable=wm_var, width=40).pack(padx=15, anchor="w")
    tk.Checkbutton(root, text="递归子文件夹", variable=rec_var).pack(anchor="w", padx=15)

    tk.Button(root, text="▶ 开始处理", command=run, bg="#4CAF50",
              fg="white", width=18).pack(pady=10)

    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="图片批量处理工具")
    parser.add_argument("folder", nargs="?", help="原图文件夹")
    parser.add_argument("-o", "--output", default="成品图", help="输出文件夹")
    parser.add_argument("--max-size", type=int, default=None, help="最长边像素，如 1080")
    parser.add_argument("--quality", type=int, default=80, help="JPEG 质量 1-100")
    parser.add_argument("--fmt", default=None, help="输出格式 jpg/png/webp")
    parser.add_argument("--watermark", default=None, help="水印文字")
    parser.add_argument("-r", "--recursive", action="store_true")
    parser.add_argument("--gui", action="store_true", help="启动图形界面")
    args = parser.parse_args()

    if args.gui or not args.folder:
        launch_gui()
        return

    process_images(args.folder, args.output, max_size=args.max_size,
                   quality=args.quality, fmt=args.fmt, watermark=args.watermark,
                   recursive=args.recursive)


if __name__ == "__main__":
    main()
