#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
豆包智能去水印工具
参考油猴脚本doubao-no-watermark的实现原理
"""

import os
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageFilter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 设置控制台输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class DoubaoSmartRemover:
    """豆包智能去水印器 - 基于油猴脚本原理"""

    def __init__(self):
        """初始化"""
        pass

    def _imread_cv2(self, image_path):
        """使用PIL读取图片，支持中文路径"""
        try:
            img_pil = Image.open(str(image_path))
            img_np = np.array(img_pil)
            if len(img_np.shape) == 3 and img_np.shape[2] == 3:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            return img_np
        except Exception as e:
            raise ValueError(f"无法读取图片 {image_path}: {str(e)}")

    def _imwrite_cv2(self, output_path, img):
        """使用PIL保存图片，支持中文路径"""
        try:
            from PIL import Image
            if len(img.shape) == 3 and img.shape[2] == 3:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                img_rgb = img
            img_pil = Image.fromarray(img_rgb)
            img_pil.save(str(output_path))
        except Exception as e:
            raise ValueError(f"无法保存图片 {output_path}: {str(e)}")

    def detect_watermark_region(self, image_path):
        """
        智能检测水印区域
        参考油猴脚本的检测逻辑
        """
        img = self._imread_cv2(image_path)
        h, w = img.shape[:2]

        # 豆包水印通常在右下角
        # 检测右下角的文字区域

        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 右下角区域（通常水印位置）
        # 豆包水印"豆包AI生成"大约占宽度的1/4到1/3
        right_region_width = int(w * 0.35)
        right_region_height = int(h * 0.15)

        # 提取右下角区域
        right_bottom = gray[h-right_region_height:h, w-right_region_width:w]

        # 使用阈值检测浅色文字（水印通常是白色或浅色）
        _, thresh = cv2.threshold(right_bottom, 200, 255, cv2.THRESH_BINARY)

        # 查找轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # 找到最大的轮廓区域
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w_contour, h_contour = cv2.boundingRect(largest_contour)

            # 转换到原图坐标
            x1 = w - right_region_width + x - 20  # 左边扩展
            y1 = h - right_region_height + y - 20  # 上边扩展
            x2 = w - right_region_width + x + w_contour + 20  # 右边扩展
            y2 = h - right_region_height + y + h_contour + 20  # 下边扩展

            # 确保在图片范围内
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)

            print(f"智能检测到水印区域: ({x1}, {y1}) -> ({x2}, {y2})")
            return [(x1, y1, x2, y2)]
        else:
            # 如果检测失败，使用默认的右下角固定区域
            print("未检测到明确水印，使用默认右下角区域")
            default_width = 500
            default_height = 100
            x1 = max(0, w - default_width - 20)
            y1 = max(0, h - default_height - 20)
            x2 = w - 20
            y2 = h - 20
            return [(x1, y1, x2, y2)]

    def remove_watermark_inpainting(self, image_path, output_path):
        """
        使用inpainting去除水印
        结合油猴脚本和OpenCV的最优方法
        """
        # 检测水印区域
        regions = self.detect_watermark_region(image_path)

        # 读取图片
        img = self._imread_cv2(image_path)
        h, w = img.shape[:2]

        # 创建mask
        mask = np.zeros((h, w), dtype=np.uint8)

        # 标记水印区域
        for (x1, y1, x2, y2) in regions:
            # 扩展区域确保完全覆盖
            x1 = max(0, x1 - 15)
            y1 = max(0, y1 - 15)
            x2 = min(w, x2 + 15)
            y2 = min(h, y2 + 15)

            # 创建渐变mask让修复更自然
            mask[y1:y2, x1:x2] = 255

        # 使用NS算法修复（质量更高）
        print("使用NS算法进行inpainting...")
        result = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)

        # 保存结果
        self._imwrite_cv2(output_path, result)
        return True


class DoubaoSmartRemoverGUI:
    """豆包智能去水印GUI"""

    def __init__(self, root):
        """初始化GUI"""
        self.root = root
        self.root.title("豆包智能去水印工具 - 油猴脚本版")
        self.root.geometry("700x650")

        self.input_files = []
        self.output_dir = Path.cwd()
        self.remover = DoubaoSmartRemover()

        self.create_widgets()

    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="豆包智能去水印工具 - 油猴脚本版",
            font=("Arial", 14, "bold"),
            fg="#4CAF50"
        )
        title_label.pack(pady=10)

        # 说明
        desc_label = tk.Label(
            self.root,
            text="基于油猴脚本doubao-no-watermark原理，智能检测并去除豆包水印",
            font=("Arial", 10),
            fg="gray"
        )
        desc_label.pack(pady=5)

        # 主框架
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 选择文件
        select_btn = tk.Button(
            main_frame,
            text="选择带水印的豆包图片",
            command=self.select_files,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=30
        )
        select_btn.pack(pady=10)

        # 文件列表
        self.files_listbox = tk.Listbox(
            main_frame,
            height=4,
            font=("Arial", 10)
        )
        self.files_listbox.pack(fill=tk.X, pady=(0, 10))

        # 输出目录
        output_frame = tk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=10)

        tk.Label(output_frame, text="输出目录:", font=("Arial", 11)).pack(side=tk.LEFT)
        self.output_dir_label = tk.Label(output_frame, text=str(self.output_dir), font=("Arial", 10), fg="blue")
        self.output_dir_label.pack(side=tk.LEFT, padx=10)
        tk.Button(output_frame, text="浏览", command=self.select_output_dir, font=("Arial", 10)).pack(side=tk.RIGHT)

        # 处理按钮
        process_btn = tk.Button(
            main_frame,
            text="开始智能去水印（油猴脚本原理）",
            command=self.process_images,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            width=35
        )
        process_btn.pack(pady=15)

        # 进度
        self.progress = ttk.Progressbar(main_frame, mode='determinate', length=600)
        self.progress.pack(pady=10)

        self.status_label = tk.Label(main_frame, text="就绪", font=("Arial", 10), fg="green")
        self.status_label.pack(pady=5)

        # 日志
        log_frame = tk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(log_frame, text="处理日志:", font=("Arial", 10)).pack(anchor=tk.W)
        self.log_text = tk.Text(log_frame, height=10, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)

    def select_files(self):
        """选择文件"""
        files = filedialog.askopenfilenames(
            title="选择带豆包水印的图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp"), ("所有文件", "*.*")]
        )

        if files:
            self.input_files = list(files)
            self.files_listbox.delete(0, tk.END)
            for file in self.input_files:
                self.files_listbox.insert(tk.END, Path(file).name)
            self.log(f"已选择 {len(self.input_files)} 个文件\n")

    def select_output_dir(self):
        """选择输出目录"""
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir = Path(dir_path)
            self.output_dir_label.config(text=str(self.output_dir))
            self.log(f"输出目录: {self.output_dir}\n")

    def process_images(self):
        """处理图片"""
        if not self.input_files:
            messagebox.showwarning("警告", "请先选择图片！")
            return

        total = len(self.input_files)
        self.progress['maximum'] = total
        self.progress['value'] = 0

        success_count = 0

        for i, file_path in enumerate(self.input_files):
            try:
                file_path = Path(file_path)
                output_path = self.output_dir / f"{file_path.stem}_smart_clean{file_path.suffix}"

                self.status_label.config(text=f"处理: {file_path.name}")
                self.log(f"\n处理 [{i+1}/{total}]: {file_path.name}\n")
                self.log("智能检测水印位置...\n")

                # 去除水印
                success = self.remover.remove_watermark_inpainting(file_path, output_path)

                if success:
                    self.log(f"✅ 成功！水印已去除，保存为: {output_path.name}\n")
                    success_count += 1
                else:
                    self.log(f"❌ 失败\n")

            except Exception as e:
                self.log(f"❌ 失败: {str(e)}\n")

            self.progress['value'] = i + 1
            self.root.update()

        self.status_label.config(text="完成")
        self.log(f"\n{'='*60}\n")
        self.log(f"处理完成！成功: {success_count}/{total}\n")
        self.log(f"输出目录: {self.output_dir}\n")
        self.log(f"{'='*60}\n")

        messagebox.showinfo("完成", f"处理完成！\n成功: {success_count}/{total}\n输出: {self.output_dir}")

    def log(self, message):
        """输出日志"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)


def main():
    """主函数"""
    print("=" * 80)
    print("              [豆包智能去水印工具 - 油猴脚本版]")
    print("=" * 80)
    print()
    print("基于油猴脚本doubao-no-watermark的实现原理")
    print("智能检测水印位置并去除")
    print()

    root = tk.Tk()
    app = DoubaoSmartRemoverGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
