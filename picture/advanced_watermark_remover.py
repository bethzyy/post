#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高级去水印工具 - 集成多种SOTA算法
结合油猴脚本智能检测 + 多种Inpainting算法
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

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class AdvancedWatermarkRemover:
    """高级去水印器 - 集成多种算法"""

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

    def smart_detect_watermark(self, image_path):
        """
        智能检测水印区域
        结合油猴脚本 + OpenCV轮廓检测
        """
        img = self._imread_cv2(image_path)
        h, w = img.shape[:2]

        print(f"[检测] 图片尺寸: {w}x{h}")

        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 右下角区域（豆包水印通常位置）
        right_region_width = int(w * 0.35)
        right_region_height = int(h * 0.15)
        right_region_width = max(400, min(right_region_width, 600))
        right_region_height = max(80, min(right_region_height, 150))

        y_start = max(0, h - right_region_height)
        x_start = max(0, w - right_region_width)
        right_bottom = gray[y_start:h, x_start:w]

        # 多种检测方法结合
        detection_methods = []

        # 方法1: 阈值检测
        _, thresh = cv2.threshold(right_bottom, 200, 255, cv2.THRESH_BINARY)
        contours1, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 方法2: 边缘检测
        edges = cv2.Canny(right_bottom, 50, 150)
        contours2, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 合并检测结果
        all_contours = []
        if contours1:
            all_contours.extend([c for c in contours1 if cv2.contourArea(c) > 100])
        if contours2:
            all_contours.extend([c for c in contours2 if cv2.contourArea(c) > 100])

        if all_contours:
            # 合并所有轮廓
            all_points = np.vstack([cnt for cnt in all_contours])
            x, y, w_contour, h_contour = cv2.boundingRect(all_points)

            # 转换到原图坐标并扩展
            x1 = x_start + x - 30
            y1 = y_start + y - 30
            x2 = x_start + x + w_contour + 30
            y2 = y_start + y + h_contour + 30

            # 确保在图片范围内
            x1 = max(0, min(x1, w))
            y1 = max(0, min(y1, h))
            x2 = max(0, min(x2, w))
            y2 = max(0, min(y2, h))

            print(f"[检测] 智能轮廓检测成功")
            print(f"[检测] 水印区域: ({x1}, {y1}) -> ({x2}, {y2})")
            print(f"[检测] 区域大小: {x2-x1}x{y2-y1}")
            return [(x1, y1, x2, y2)], "智能检测"

        # 降级：动态固定区域
        print(f"[检测] 轮廓检测失败，使用动态固定区域")
        text_height = min(100, int(h * 0.12))
        text_width = min(500, int(w * 0.30))
        margin_right = 20
        margin_bottom = 20

        x1 = max(0, w - text_width - margin_right)
        y1 = max(0, h - text_height - margin_bottom)
        x2 = w - margin_right
        y2 = h - margin_bottom

        print(f"[检测] 固定区域: ({x1}, {y1}) -> ({x2}, {y2})")
        return [(x1, y1, x2, y2)], "固定区域"

    def inpaint_telea(self, img, mask):
        """Telea算法 - 快速"""
        return cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    def inpaint_ns(self, img, mask):
        """NS算法 - 高质量"""
        return cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)

    def inpaint_hybrid(self, img, mask):
        """混合算法 - 结合Telea和NS"""
        result_telea = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        result_ns = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)

        # 加权平均
        result = cv2.addWeighted(result_telea, 0.4, result_ns, 0.6, 0)
        return result

    def inpaint_advanced(self, img, mask):
        """高级算法 - 多次迭代"""
        # 第一次：NS算法
        result = cv2.inpaint(img, mask, 5, cv2.INPAINT_NS)

        # 第二次：对结果进行轻微模糊
        blurred = cv2.GaussianBlur(result, (3, 3), 0)

        # 第三次：边缘保持
        edges = cv2.Canny(result, 50, 150)
        edges = cv2.dilate(edges, None, iterations=1)

        # 在边缘区域使用原始图像
        result_edges = cv2.inpaint(blurred, edges, 3, cv2.INPAINT_TELEA)

        return result_edges

    def remove_watermark_best_quality(self, image_path, output_dir):
        """
        使用最佳质量方法去除水印
        只生成NS高质量版本
        """
        # 检测水印
        regions, method = self.smart_detect_watermark(image_path)

        if not regions:
            print("[错误] 未检测到水印区域")
            return None

        img = self._imread_cv2(image_path)
        h, w = img.shape[:2]

        # 创建mask
        mask = np.zeros((h, w), dtype=np.uint8)
        for (x1, y1, x2, y2) in regions:
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            # 扩展区域确保完全覆盖
            x1 = max(0, x1 - 15)
            y1 = max(0, y1 - 15)
            x2 = min(w, x2 + 15)
            y2 = min(h, y2 + 15)
            mask[y1:y2, x1:x2] = 255

        # 使用NS高质量算法
        try:
            print(f"[处理] 使用NS高质量算法...")
            result = self.inpaint_ns(img, mask)

            # 保存结果 - 使用原文件名
            image_path = Path(image_path)
            output_dir = Path(output_dir)
            output_name = f"{image_path.stem}{image_path.suffix}"
            output_path = output_dir / output_name
            self._imwrite_cv2(output_path, result)

            print(f"[成功] 已保存: {output_path.name}")
            return output_path

        except Exception as e:
            print(f"[错误] 处理失败: {str(e)}")
            return None


class AdvancedWatermarkRemoverGUI:
    """高级去水印GUI"""

    def __init__(self, root):
        """初始化GUI"""
        self.root = root
        self.root.title("高级去水印工具 - NS高质量版")
        self.root.geometry("700x650")

        self.input_files = []
        self.output_dir = Path.cwd() / "output"  # 默认保存到output子目录
        self.remover = AdvancedWatermarkRemover()

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.create_widgets()

    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="高级去水印工具 - NS高质量版",
            font=("Arial", 14, "bold"),
            fg="#2196F3"
        )
        title_label.pack(pady=10)

        # 说明
        desc_text = "集成油猴脚本智能检测 + OpenCV NS高质量算法\n自动生成最佳质量的无水印图片"
        desc_label = tk.Label(
            self.root,
            text=desc_text,
            font=("Arial", 10),
            fg="gray",
            justify=tk.CENTER
        )
        desc_label.pack(pady=5)

        # 主框架
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 选择文件
        select_btn = tk.Button(
            main_frame,
            text="选择带水印的图片",
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

        # 算法说明
        algo_frame = tk.LabelFrame(main_frame, text="算法说明", font=("Arial", 10, "bold"), padx=10, pady=10)
        algo_frame.pack(fill=tk.X, pady=10)

        algo_text = """• 智能检测: 油猴脚本原理 + OpenCV轮廓检测
• NS算法: Navier-Stokes方程，质量最高
• 特点: 自然修复，几乎无痕迹
• 适用: 复杂背景，专业用途"""

        tk.Label(algo_frame, text=algo_text, font=("Consolas", 9), justify=tk.LEFT).pack(anchor=tk.W)

        # 处理按钮
        process_btn = tk.Button(
            main_frame,
            text="开始去水印（NS高质量算法）",
            command=self.process_images,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            width=35
        )
        process_btn.pack(pady=15)

        # 进度
        self.progress = ttk.Progressbar(main_frame, mode='determinate', length=650)
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
            title="选择带水印的图片",
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

                self.status_label.config(text=f"处理: {file_path.name}")
                self.log(f"\n{'='*60}\n")
                self.log(f"[{i+1}/{total}] 处理: {file_path.name}\n")
                self.log(f"{'='*60}\n")

                # 去除水印（NS高质量）
                output_path = self.remover.remove_watermark_best_quality(file_path, self.output_dir)

                if output_path:
                    self.log(f"\n✅ 成功! 水印已去除\n")
                    self.log(f"   输出: {output_path.name}\n")
                    success_count += 1
                else:
                    self.log(f"\n❌ 失败\n")

            except Exception as e:
                self.log(f"\n❌ 错误: {str(e)}\n")

            self.progress['value'] = i + 1
            self.root.update()

        self.status_label.config(text="完成")
        self.log(f"\n{'='*60}\n")
        self.log(f"处理完成! 成功: {success_count}/{total}\n")
        self.log(f"输出目录: {self.output_dir}\n")
        self.log(f"{'='*60}\n")

        messagebox.showinfo(
            "完成",
            f"处理完成！\n成功: {success_count}/{total}\n输出: {self.output_dir}"
        )

    def log(self, message):
        """输出日志"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)


def main():
    """主函数"""
    print("=" * 80)
    print("              [高级去水印工具 - NS高质量版]")
    print("=" * 80)
    print()
    print("集成技术:")
    print("  • 油猴脚本智能检测")
    print("  • OpenCV NS高质量算法")
    print("  • Navier-Stokes方程")
    print("  • 自然修复，几乎无痕迹")
    print()

    root = tk.Tk()
    app = AdvancedWatermarkRemoverGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
