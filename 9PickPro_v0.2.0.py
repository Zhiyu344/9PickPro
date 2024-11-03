import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import os
import random

class _9PickPro:
    def __init__(self, root):
        self.root = root
        self.version = "0.2.0"  # 定义版本信息
        self.root.title(f"9PickPro v{self.version}")
        
        # 设置窗口初始大小
        self.root.geometry("400x400")  # 设置窗口大小为 400x400 像素
        
        # 创建菜单
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="导入名单", command=self.import_lists)
        filemenu.add_command(label="退出", command=root.quit)
        menubar.add_cascade(label="文件", menu=filemenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=helpmenu)
        root.config(menu=menubar)
        
        # 名单数据
        self.lists = {}

        # 选择名单标签
        self.list_label = tk.Label(root, text="选择名单:")
        self.list_label.pack(pady=5)  # 打包标签

        # 下拉框
        self.list_var = tk.StringVar()
        self.list_dropdown = None
        self.update_dropdown()  # 更新下拉框

        # 抽取次数输入框
        self.count_label = tk.Label(root, text="抽取次数:")
        self.count_entry = tk.Entry(root)
        
        # 开始按钮
        self.start_button = tk.Button(root, text="确定", command=self.start_Pick)
        
        # 结果显示框
        self.result_text = tk.Text(root, height=10, width=40, state='disabled')
        
        # 打包组件
        self.count_label.pack(pady=5)
        self.list_dropdown.pack(pady=5)
        self.count_entry.pack(pady=5)
        self.start_button.pack(pady=10)
        self.result_text.pack(pady=10)

    def import_lists(self):
        filepaths = filedialog.askopenfilenames(filetypes=[("DAT files", "*.dat")])
        if not filepaths:
            return

        for filepath in filepaths:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                members = [line.strip() for line in lines if line.strip()]
            list_title = simpledialog.askstring("设置名单标题", f"请输入 {os.path.basename(filepath)} 的名单标题:")
            if list_title:
                self.lists[list_title] = members
        self.update_dropdown()

    def update_dropdown(self):
        if hasattr(self, 'list_dropdown') and self.list_dropdown:
            self.list_dropdown.destroy()  # 删除旧的下拉框
        
        if self.lists:
            style = ttk.Style()
            style.configure('TCombobox', foreground='black', background='white', fieldbackground='white')
            style.map('TCombobox', fieldbackground=[('readonly', 'white')])
            
            self.list_dropdown = ttk.Combobox(self.root, textvariable=self.list_var, values=list(self.lists.keys()), state='readonly')
        else:
            self.list_var.set("无名单")
            style = ttk.Style()
            style.configure('TCombobox', foreground='gray', background='white', fieldbackground='white')
            style.map('TCombobox', fieldbackground=[('readonly', 'white')])
            
            self.list_dropdown = ttk.Combobox(self.root, textvariable=self.list_var, values=[], state='readonly')
        
        # 重新打包下拉框
        self.list_dropdown.pack(pady=5)

    def start_Pick(self):
        selected_list = self.list_var.get()
        if not selected_list:
            messagebox.showerror("错误", "请选择一个名单！")
            return

        pick_count = self.count_entry.get()
        if not pick_count.isdigit() or int(pick_count) <= 0:
            messagebox.showerror("错误", "请输入有效的抽取次数！")
            return

        pick_count = int(pick_count)
        members = self.lists[selected_list]

        if pick_count > len(members):
            messagebox.showerror("错误", "抽取次数超过了名单中的成员数量！")
            return

        picked_members = random.sample(members, pick_count)

        # 临时启用 Text 组件
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "抽取结果:\n")
        for member in picked_members:
            self.result_text.insert(tk.END, f"{member}\n")
        # 禁用 Text 组件
        self.result_text.config(state='disabled')

    def show_about(self):
        messagebox.showinfo("关于", f"9PickPro v{self.version}\n一款小而美的抽奖应用程序\n版权所有 © 2024 9Imprint")

if __name__ == "__main__":
    root = tk.Tk()
    app = _9PickPro(root)
    root.mainloop()
