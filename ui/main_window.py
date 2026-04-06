import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, root, back_login, show_list, show_new_record, show_query):
        self.root = root
        self.back_login = back_login
        self.show_list = show_list
        self.show_new_record = show_new_record
        self.show_query = show_query
        self.root.title("苏凤阁 - 医疗服务主菜单")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        self.root.config(bg="#f0f4f8")

        # 顶部导航栏
        top_frame = tk.Frame(root, bg="#1a237e", height=90)
        top_frame.pack(fill=tk.X, anchor=tk.N)
        top_frame.pack_propagate(False)
        tk.Label(
            top_frame,
            text="苏凤阁医疗服务系统 - 主菜单",
            font=("微软雅黑", 22, "bold"),
            fg="white",
            bg="#1a237e"
        ).pack(pady=22)

        # 功能按钮区
        content_frame = tk.Frame(root, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=40)
        btn_container = tk.Frame(content_frame, bg="#f0f4f8")
        btn_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 主按钮统一样式（高对比度，字体绝对清晰）
        btn_style = {
            "font": ("微软雅黑", 16, "bold"),
            "bg": "#2196F3",
            "fg": "white",
            "activebackground": "#1976D2",
            "activeforeground": "white",
            "width": 12,
            "bd": 0,
            "relief": tk.FLAT,
            "padx": 15,
            "pady": 12
        }

        # 退出登录按钮样式
        logout_btn_style = {
            "font": ("微软雅黑", 12, "bold"),
            "bg": "#f44336",
            "fg": "white",
            "activebackground": "#d32f2f",
            "activeforeground": "white",
            "width": 10,
            "bd": 0,
            "relief": tk.FLAT,
            "padx": 8,
            "pady": 4
        }

        # 功能按钮（原生tk.Button，无报错，字体清晰）
        self.btn1 = tk.Button(btn_container, text="中药", command=lambda: self.show_list("中药"), **btn_style)
        self.btn2 = tk.Button(btn_container, text="西药", command=lambda: self.show_list("西药"), **btn_style)
        self.btn3 = tk.Button(btn_container, text="疼痛", command=lambda: self.show_list("疼痛"), **btn_style)
        self.btn4 = tk.Button(btn_container, text="新建病历", command=self.show_new_record, **btn_style)
        self.btn5 = tk.Button(btn_container, text="历史病历查询", command=self.show_query, **btn_style)

        # 网格布局
        self.btn1.grid(row=0, column=0, padx=25, pady=25)
        self.btn2.grid(row=0, column=1, padx=25, pady=25)
        self.btn3.grid(row=0, column=2, padx=25, pady=25)
        self.btn4.grid(row=1, column=0, padx=25, pady=25)
        self.btn5.grid(row=1, column=1, padx=25, pady=25)

        # 底部退出按钮
        bottom_frame = tk.Frame(root, bg="#f0f4f8", height=70)
        bottom_frame.pack(fill=tk.X, anchor=tk.S)
        bottom_frame.pack_propagate(False)
        tk.Button(
            bottom_frame,
            text="退出登录",
            command=self.logout,
            **logout_btn_style
        ).pack(side=tk.RIGHT, padx=40, pady=15)

    def logout(self):
        self.root.destroy()
        self.back_login()