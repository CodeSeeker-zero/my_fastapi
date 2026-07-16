import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# 支持的视频后缀
VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".rmvb", ".m4v"}


class VideoRenameTool:
    def __init__(self, root):
        self.root = root
        self.root.title("视频批量正则重命名工具（支持子文件夹递归）")
        self.root.geometry("720x520")

        # 存储选中文件夹
        self.folder_path = tk.StringVar()
        # 正则匹配表达式
        self.regex_pattern = tk.StringVar()
        # 替换文本
        self.replace_text = tk.StringVar()
        # 是否递归遍历子文件夹
        self.is_recursive = tk.BooleanVar(value=True)
        # 待修改文件列表：(文件完整路径, 原文件名, 新文件名)
        self.file_list = []

        self.create_widgets()

    def create_widgets(self):
        # 1. 文件夹选择区域
        frame1 = tk.Frame(self.root, pady=8)
        frame1.pack(fill="x", padx=10)
        tk.Label(frame1, text="目标根文件夹：").pack(side="left")
        tk.Entry(frame1, textvariable=self.folder_path, width=50).pack(
            side="left", padx=5
        )
        tk.Button(frame1, text="选择", command=self.select_folder).pack(side="left")

        # 递归勾选框
        frame_recur = tk.Frame(self.root, pady=2)
        frame_recur.pack(fill="x", padx=10)
        tk.Checkbutton(
            frame_recur, text="递归遍历所有子文件夹内视频", variable=self.is_recursive
        ).pack(side="left")

        # 2. 正则输入区域
        frame2 = tk.Frame(self.root, pady=8)
        frame2.pack(fill="x", padx=10)
        tk.Label(frame2, text="正则匹配：", width=10).pack(side="left")
        tk.Entry(frame2, textvariable=self.regex_pattern, width=32).pack(
            side="left", padx=5
        )
        tk.Label(frame2, text="替换为：", width=8).pack(side="left", padx=5)
        tk.Entry(frame2, textvariable=self.replace_text, width=24).pack(side="left")

        # 3. 操作按钮
        frame3 = tk.Frame(self.root, pady=5)
        frame3.pack()
        tk.Button(
            frame3, text="预览修改结果", command=self.preview_rename, bg="#cce5ff"
        ).pack(side="left", padx=8)
        tk.Button(
            frame3, text="执行批量重命名", command=self.do_rename, bg="#ffcccc"
        ).pack(side="left", padx=8)
        tk.Button(frame3, text="清空日志", command=self.clear_log).pack(
            side="left", padx=8
        )

        # 4. 日志预览框
        tk.Label(self.root, text="修改预览/运行日志（含文件路径）：").pack()
        self.log_text = scrolledtext.ScrolledText(self.root, width=90, height=18)
        self.log_text.pack(padx=10, pady=5)

    def select_folder(self):
        """选择根文件夹"""
        path = filedialog.askdirectory(title="选择存放视频的根文件夹（包含子文件夹）")
        if path:
            self.folder_path.set(path)
            self.log_text.insert(tk.END, f"已选择根目录：{path}\n")
            self.log_text.see(tk.END)

    def get_video_files_recursive(self):
        """递归获取所有视频文件，返回 [(文件夹路径, 文件名)]"""
        root_dir = self.folder_path.get().strip()
        if not root_dir or not os.path.isdir(root_dir):
            messagebox.showerror("错误", "请先选择有效文件夹！")
            return []

        video_info = []
        # 选择递归 or 仅当前目录
        if self.is_recursive.get():
            walk_iter = os.walk(root_dir)
        else:
            # 只遍历一层，模拟walk格式
            walk_iter = [(root_dir, [], os.listdir(root_dir))]

        for dirpath, _, filenames in walk_iter:
            for fname in filenames:
                full_path = os.path.join(dirpath, fname)
                if os.path.isfile(full_path):
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in VIDEO_EXT:
                        video_info.append((dirpath, fname))
        return video_info

    def preview_rename(self):
        """预览替换结果，不实际修改"""
        self.log_text.delete(1.0, tk.END)
        pattern_str = self.regex_pattern.get().strip()
        if not pattern_str:
            messagebox.showwarning("提示", "请输入正则匹配表达式！")
            return
        try:
            pat = re.compile(pattern_str)
        except re.error as e:
            messagebox.showerror("正则表达式错误", f"正则语法有误：{str(e)}")
            return

        self.file_list = []
        video_all = self.get_video_files_recursive()
        if not video_all:
            self.log_text.insert(tk.END, "目录（含子文件夹）内未找到任何视频文件\n")
            return

        self.log_text.insert(
            tk.END, "===== 预览修改列表（路径 | 原文件名 → 新文件名）=====\n\n"
        )
        replace_str = self.replace_text.get()
        for dir_path, old_name in video_all:
            name_no_ext, ext = os.path.splitext(old_name)
            new_name_no_ext = pat.sub(replace_str, name_no_ext)
            new_full_name = new_name_no_ext + ext
            if old_name == new_full_name:
                continue
            # 保存完整路径信息用于后续重命名
            old_full_path = os.path.join(dir_path, old_name)
            self.file_list.append((dir_path, old_name, new_full_name))
            self.log_text.insert(
                tk.END, f"[{dir_path}]\n{old_name}  →  {new_full_name}\n\n"
            )

        if not self.file_list:
            self.log_text.insert(tk.END, "\n无匹配需要修改的文件\n")
        else:
            self.log_text.insert(
                tk.END, f"\n总计待修改文件：{len(self.file_list)} 个\n"
            )
        self.log_text.see(tk.END)

    def do_rename(self):
        """执行真实重命名（支持多层子目录）"""
        if not self.file_list:
            messagebox.showinfo("提示", "请先点击【预览修改结果】加载文件列表！")
            return
        confirm = messagebox.askyesno(
            "确认操作",
            f"即将重命名 {len(self.file_list)} 个视频（包含子文件夹），确定继续？\n建议先备份文件！",
        )
        if not confirm:
            return

        success = 0
        fail = 0
        self.log_text.insert(tk.END, "\n===== 开始执行重命名 =====\n")
        for dir_path, old_name, new_name in self.file_list:
            old_path = os.path.join(dir_path, old_name)
            new_path = os.path.join(dir_path, new_name)
            # 防止同目录重名覆盖
            if os.path.exists(new_path):
                self.log_text.insert(
                    tk.END, f"失败：[{dir_path}] {new_name} 已存在，跳过 {old_name}\n"
                )
                fail += 1
                continue
            try:
                os.rename(old_path, new_path)
                self.log_text.insert(
                    tk.END, f"成功：[{dir_path}] {old_name} → {new_name}\n"
                )
                success += 1
            except Exception as e:
                self.log_text.insert(
                    tk.END, f"失败 [{dir_path}] {old_name}：{str(e)}\n"
                )
                fail += 1
        self.log_text.insert(
            tk.END, f"\n操作完成！成功：{success} 个，失败：{fail} 个\n"
        )
        self.log_text.see(tk.END)
        messagebox.showinfo("完成", f"重命名结束\n成功：{success}\n失败：{fail}")
        self.file_list = []

    def clear_log(self):
        """清空日志框"""
        self.log_text.delete(1.0, tk.END)


if __name__ == "__main__":
    window = tk.Tk()
    app = VideoRenameTool(window)
    window.mainloop()
