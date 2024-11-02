import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import random
import os

class _9PickPro:
    def __init__(self, root):
        self.root = root
        self.version = "0.1.0"  # 定义版本信息
        self.root.title(f"9PickPro v{self.version}")
        
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

        # 下拉框
        self.list_var = tk.StringVar()
        self.list_dropdown = None  # 初始化时不创建 OptionMenu
        self.update_dropdown()  # 更新下拉框

        # 抽取次数输入框
        self.count_label = tk.Label(root, text="抽取次数:")
        self.count_label.pack()
        self.count_entry = tk.Entry(root)
        self.count_entry.pack(pady=5)

        # 开始按钮
        self.start_button = tk.Button(root, text="确定", command=self.start_Pick)
        self.start_button.pack(pady=10)

        # 结果显示框
        self.result_text = tk.Text(root, height=10, width=40)
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
        if self.list_dropdown:
            self.list_dropdown.destroy()

        if self.lists:
            self.list_var.set(next(iter(self.lists.keys())))
            self.list_dropdown = tk.OptionMenu(self.root, self.list_var, *self.lists.keys(), command=self.update_list)
            self.list_dropdown.pack(pady=5)
        else:
            self.list_dropdown = None

    def update_list(self, value):
        self.list_var.set(value)

    def start_Pick(self):
        list_name = self.list_var.get()
        if not list_name:
            messagebox.showerror("错误", "请选择一个名单")
            return
        
        try:
            count = int(self.count_entry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的 Pick 次数")
            return

        if count <= 0:
            messagebox.showerror("错误", "Pick 次数必须大于0")
            return

        if not self.lists[list_name]:
            messagebox.showwarning("警告", f"{list_name} 没有成员")
            return

        results = random.sample(self.lists[list_name], min(count, len(self.lists[list_name])))
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "\n".join(results))

    def show_about(self):
        about_message = f"9PickPro v{self.version}\n\n这是一个小巧的、用于随机抽取名单的应用程序。\n\n版权所有 © 2024 9Imprint"
        messagebox.showinfo("关于", about_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = _9PickPro(root)
    root.mainloop()
