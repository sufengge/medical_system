import tkinter as tk
from tkinter import ttk, messagebox
from core.user_manager import UserManager


class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.um = UserManager()
        self.root.title("医疗服务系统-技术支持：苏凤阁 18729762991")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # 主背景：柔和浅蓝灰，护眼不刺眼
        main_frame = tk.Frame(root, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # 品牌LOGO：深靛蓝粗体，清晰醒目
        tk.Label(main_frame, text="医疗服务系统-技术支持：苏凤阁 18729762991",
                 font=("微软雅黑", 28, "bold"), fg="#1a237e", bg="#f0f4f8") \
            .pack(pady=35)

        # 登录卡片：纯白背景+深色边框，对比明显
        login_card = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SOLID, padx=40, pady=30)
        login_card.pack(padx=60, pady=10, fill=tk.BOTH, expand=True)

        # 用户名标签&输入框
        tk.Label(login_card, text="用户名", font=("微软雅黑", 14, "bold"), bg="white", fg="#1a237e").pack(pady=(20, 8))
        self.user_entry = ttk.Entry(login_card, font=("微软雅黑", 13), width=32)
        self.user_entry.pack(pady=(0, 18))

        # 密码标签&输入框
        tk.Label(login_card, text="密码", font=("微软雅黑", 14, "bold"), bg="white", fg="#1a237e").pack(pady=(8, 8))
        self.pwd_entry = ttk.Entry(login_card, font=("微软雅黑", 13), width=32, show="●")
        self.pwd_entry.pack(pady=(0, 25))

        # 按钮区：原生tk.Button，样式100%生效，高对比度
        btn_frame = tk.Frame(login_card, bg="white")
        btn_frame.pack(pady=10)

        # 按钮样式统一配置（深蓝背景+纯白粗体，hover加深）
        btn_style = {
            "font": ("微软雅黑", 13, "bold"),
            "bg": "#2196F3",  # 主色：专业医疗蓝
            "fg": "white",  # 字体：纯白，绝对清晰
            "activebackground": "#1976D2",  # 鼠标悬浮：更深的蓝
            "activeforeground": "white",
            "width": 12,
            "bd": 0,  # 无边框，现代扁平风格
            "relief": tk.FLAT,
            "padx": 10,
            "pady": 8
        }

        # 三个核心操作按钮
        tk.Button(btn_frame, text="登录", command=self.login, **btn_style).grid(row=0, column=0, padx=15)
        tk.Button(btn_frame, text="注册", command=self.show_register, **btn_style).grid(row=0, column=1, padx=15)
        tk.Button(btn_frame, text="忘记密码", command=self.show_forget, **btn_style).grid(row=0, column=2, padx=15)

    # 登录逻辑（完全保留原有功能）
    def login(self):
        user = self.user_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        if not user or not pwd:
            messagebox.showwarning("提示", "请输入用户名和密码！")
            return
        ok, msg = self.um.login(user, pwd)
        if ok:
            messagebox.showinfo("成功", msg)
            self.on_success()
        else:
            messagebox.showerror("失败", msg)

    # 注册弹窗（样式同步优化）
    def show_register(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("用户注册 - 医疗服务系统")
        reg_win.geometry("420x380")
        reg_win.resizable(False, False)
        reg_win.grab_set()
        frame = tk.Frame(reg_win, bg="#f0f4f8")
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        tk.Label(frame, text="用户注册", font=("微软雅黑", 16, "bold"), fg="#1a237e", bg="#f0f4f8").pack(pady=10)
        tk.Label(frame, text="用户名", font=("微软雅黑", 12), bg="#f0f4f8", fg="#1a237e").pack(pady=(15, 5))
        u = ttk.Entry(frame, font=("微软雅黑", 12), width=25)
        u.pack(pady=(0, 8))
        tk.Label(frame, text="密码", font=("微软雅黑", 12), bg="#f0f4f8", fg="#1a237e").pack(pady=(8, 5))
        p = ttk.Entry(frame, font=("微软雅黑", 12), width=25, show="●")
        p.pack(pady=(0, 8))
        tk.Label(frame, text="手机号", font=("微软雅黑", 12), bg="#f0f4f8", fg="#1a237e").pack(pady=(8, 5))
        ph = ttk.Entry(frame, font=("微软雅黑", 12), width=25)
        ph.pack(pady=(0, 15))

        # 注册按钮（样式统一）
        def do_reg():
            if not all([u.get().strip(), p.get().strip(), ph.get().strip()]):
                messagebox.showwarning("提示", "请填写完整信息！")
                return
            ok, msg = self.um.register(u.get().strip(), p.get().strip(), ph.get().strip())
            messagebox.showinfo("结果", msg)
            if ok: reg_win.destroy()

        tk.Button(frame, text="确认注册", command=do_reg,
                  font=("微软雅黑", 12, "bold"), bg="#2196F3", fg="white",
                  activebackground="#1976D2", activeforeground="white",
                  width=15, bd=0, relief=tk.FLAT, padx=8, pady=6).pack(pady=10)

    # 忘记密码弹窗（样式同步优化）
    def show_forget(self):
        f_win = tk.Toplevel(self.root)
        f_win.title("找回密码 - 医疗服务系统")
        f_win.geometry("420x400")
        f_win.resizable(False, False)
        f_win.grab_set()
        frame = tk.Frame(f_win, bg="#f0f4f8")
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        tk.Label(frame, text="找回密码", font=("微软雅黑", 16, "bold"), fg="#1a237e", bg="#f0f4f8").pack(pady=10)
        tk.Label(frame, text="手机号", font=("微软雅黑", 12), bg="#f0f4f8", fg="#1a237e").pack(pady=(15, 5))
        phone = ttk.Entry(frame, font=("微软雅黑", 12), width=25)
        phone.pack(pady=(0, 8))

        code_frame = tk.Frame(frame, bg="#f0f4f8")
        code_frame.pack(fill=tk.X, pady=(8, 5))
        tk.Label(code_frame, text="验证码", font=("微软雅黑", 12), bg="#f0f4f8", fg="#1a237e").pack(side=tk.LEFT)
        code = ttk.Entry(code_frame, font=("微软雅黑", 12), width=12)
        code.pack(side=tk.LEFT, padx=10)
        # 获取验证码按钮（样式统一）
        tk.Button(code_frame, text="获取验证码", command=lambda: self.send_code(phone),
                  font=("微软雅黑", 11, "bold"), bg="#2196F3", fg="white",
                  activebackground="#1976D2", activeforeground="white",
                  bd=0, relief=tk.FLAT, padx=8, pady=4).pack(side=tk.RIGHT)

        tk.Label(frame, text="新密码", font=("微软雅黑", 12), bg="#f0f4f8", fg="#1a237e").pack(pady=(8, 5))
        new_pwd = ttk.Entry(frame, font=("微软雅黑", 12), width=25, show="●")
        new_pwd.pack(pady=(0, 15))

        def reset():
            if not all([phone.get().strip(), code.get().strip(), new_pwd.get().strip()]):
                messagebox.showwarning("提示", "请填写完整信息！")
                return
            ok, msg = self.um.reset_pwd(phone.get().strip(), code.get().strip(), new_pwd.get().strip())
            messagebox.showinfo("结果", msg)
            if ok: f_win.destroy()

        tk.Button(frame, text="重置密码", command=reset,
                  font=("微软雅黑", 12, "bold"), bg="#2196F3", fg="white",
                  activebackground="#1976D2", activeforeground="white",
                  width=15, bd=0, relief=tk.FLAT, padx=8, pady=6).pack(pady=10)

    def send_code(self, phone_entry):
        phone = phone_entry.get().strip()
        if not phone:
            messagebox.showwarning("提示", "请输入手机号！")
            return
        code = self.um.send_code(phone)
        messagebox.showinfo("验证码发送成功", f"您的验证码为：{code}\n（仅用于密码重置）")