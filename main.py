import tkinter as tk
from tkinter import ttk, messagebox
from core.user_manager import UserManager
from core.data_manager import DataManager
from ui.record_window import NewRecordWindow
from ui.query_window import QueryWindow
from ui.detail_window import DetailWindow


# --------------------- 登录窗口（完整功能版） ---------------------
class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.um = UserManager()
        self.root.title("y")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        main_frame = tk.Frame(root, bg="#F0F8FF")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        tk.Label(main_frame, text="医疗服务系统",
                 font=("微软雅黑", 24, "bold"), fg="#2E4057", bg="#F0F8FF") \
            .pack(pady=35)

        login_card = tk.Frame(main_frame, bg="white", bd=2, relief=tk.FLAT)
        login_card.pack(padx=60, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(login_card, text="用户名", font=("微软雅黑", 13), bg="white", fg="#333").pack(pady=(25, 5))
        self.user_entry = ttk.Entry(login_card, font=("微软雅黑", 13), width=28)
        self.user_entry.pack(pady=(0, 12))

        tk.Label(login_card, text="密码", font=("微软雅黑", 13), bg="white", fg="#333").pack(pady=(8, 5))
        self.pwd_entry = ttk.Entry(login_card, font=("微软雅黑", 13), width=28, show="●")
        self.pwd_entry.pack(pady=(0, 22))

        btn_frame = tk.Frame(login_card, bg="white")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="登录", command=self.login, width=10).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="注册", command=self.show_register, width=10).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="忘记密码", command=self.show_forget, width=10).grid(row=0, column=2, padx=10)

    def login(self):
        user = self.user_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        if not user or not pwd:
            messagebox.showwarning("提示", "请输入用户名密码")
            return
        ok, msg = self.um.login(user, pwd)
        if ok:
            messagebox.showinfo("成功", msg)
            self.on_success()
        else:
            messagebox.showerror("失败", msg)

    def show_register(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("用户注册")
        reg_win.geometry("420x360")
        reg_win.grab_set()
        frame = tk.Frame(reg_win, bg="#F0F8FF")
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        tk.Label(frame, text="用户注册", font=("微软雅黑", 16, "bold"), bg="#F0F8FF").pack(pady=10)
        tk.Label(frame, text="用户名").pack()
        u = ttk.Entry(frame, font=("微软雅黑", 12))
        u.pack(pady=5)
        tk.Label(frame, text="密码").pack()
        p = ttk.Entry(frame, font=("微软雅黑", 12), show="●")
        p.pack(pady=5)
        tk.Label(frame, text="手机号").pack()
        ph = ttk.Entry(frame, font=("微软雅黑", 12))
        ph.pack(pady=5)

        def do_reg():
            ok, msg = self.um.register(u.get(), p.get(), ph.get())
            messagebox.showinfo("结果" if ok else "错误", msg)
            if ok: reg_win.destroy()

        ttk.Button(frame, text="注册", command=do_reg).pack(pady=12)

    def show_forget(self):
        f_win = tk.Toplevel(self.root)
        f_win.title("找回密码")
        f_win.geometry("420x380")
        f_win.grab_set()
        frame = tk.Frame(f_win, bg="#F0F8FF")
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        tk.Label(frame, text="找回密码", font=("微软雅黑", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="手机号").pack()
        phone = ttk.Entry(frame, font=("微软雅黑", 12))
        phone.pack(pady=5)
        tk.Label(frame, text="验证码").pack()
        code = ttk.Entry(frame, font=("微软雅黑", 12))
        code.pack(pady=5)
        tk.Label(frame, text="新密码").pack()
        new_pwd = ttk.Entry(frame, font=("微软雅黑", 12), show="●")
        new_pwd.pack(pady=5)

        def send():
            if phone.get():
                messagebox.showinfo("验证码", f"验证码：{self.um.send_code(phone.get())}")

        ttk.Button(frame, text="获取验证码", command=send).pack(pady=2)

        def reset():
            ok, msg = self.um.reset_pwd(phone.get(), code.get(), new_pwd.get())
            messagebox.showinfo("结果" if ok else "错误", msg)
            if ok: f_win.destroy()

        ttk.Button(frame, text="重置密码", command=reset).pack(pady=6)


# --------------------- 主菜单（100%稳定自适应版） ---------------------
class MainWindow:
    def __init__(self, root, back_login, show_list, show_new_record, show_query):
        self.root = root
        self.back_login = back_login
        self.show_list = show_list
        self.show_new_record = show_new_record
        self.show_query = show_query
        self.root.title("医疗服务系统-技术支持：苏凤阁 18729762991")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        self.root.config(bg="#F7FBFF")

        # 顶部栏
        top_frame = tk.Frame(root, bg="#4A90E2", height=90)
        top_frame.pack(fill=tk.X, anchor=tk.N)
        top_frame.pack_propagate(False)
        tk.Label(top_frame, text="医疗服务系统", font=("微软雅黑", 24, "bold"), fg="white", bg="#4A90E2").pack(
            pady=22)

        # 主内容区（稳定布局，绝对不空白）
        content_frame = tk.Frame(root, bg="#F7FBFF")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        # 按钮容器（居中网格，自适应窗口）
        btn_container = tk.Frame(content_frame, bg="#F7FBFF")
        btn_container.pack(expand=True)

        # 按钮样式（清晰可见，不透明）
        btn_style = {
            "font": ("微软雅黑", 16, "bold"),
            "bg": "#5AA7DE",
            "fg": "white",
            "activebackground": "#4A90E2",
            "width": 12,
            "height": 2,
            "bd": 0,
            "relief": tk.FLAT
        }

        # 创建5个核心按钮
        self.btn1 = tk.Button(btn_container, text="中药", **btn_style, command=lambda: self.show_list("中药"))
        self.btn2 = tk.Button(btn_container, text="西药", **btn_style, command=lambda: self.show_list("西药"))
        self.btn3 = tk.Button(btn_container, text="疼痛", **btn_style, command=lambda: self.show_list("疼痛"))
        self.btn4 = tk.Button(btn_container, text="新建病历", **btn_style, command=self.show_new_record)
        self.btn5 = tk.Button(btn_container, text="历史病历查询", **btn_style, command=self.show_query)

        # 网格布局（绝对居中，窗口缩放自动适配）
        self.btn1.grid(row=0, column=0, padx=25, pady=25)
        self.btn2.grid(row=0, column=1, padx=25, pady=25)
        self.btn3.grid(row=0, column=2, padx=25, pady=25)
        self.btn4.grid(row=1, column=0, padx=25, pady=25)
        self.btn5.grid(row=1, column=1, padx=25, pady=25)

        # 底部退出按钮
        bottom_frame = tk.Frame(root, bg="#F7FBFF", height=70)
        bottom_frame.pack(fill=tk.X, anchor=tk.S)
        bottom_frame.pack_propagate(False)
        tk.Button(
            bottom_frame,
            text="退出登录",
            font=("微软雅黑", 12),
            bg="#FF6B6B",
            fg="white",
            width=12,
            command=self.logout
        ).pack(side=tk.RIGHT, padx=40, pady=15)

    def logout(self):
        self.root.destroy()
        self.back_login()


# --------------------- 主程序（核心修复：列表页数据加载） ---------------------
class MedicalApp:
    def __init__(self):
        self.root = tk.Tk()
        self.dm = DataManager()
        self.show_login()

    def show_login(self):
        self.clear_all()
        LoginWindow(self.root, self.show_main)

    def show_main(self):
        self.clear_all()
        MainWindow(self.root, self.show_login, self.show_list, self.show_new_record, self.show_query)

    # 核心修复：分类列表页（中药/西药/疼痛）数据加载
    def show_list(self, type_name):
        self.clear_all()
        self.root.config(bg="#F7FBFF")

        # 【关键修复】每次进入列表页，强制重新加载最新数据
        self.dm.load_records()
        records = self.dm.get_records_by_type(type_name)

        # 标题
        tk.Label(self.root, text=f"{type_name} - 病历列表", font=("微软雅黑", 18, "bold"), bg="#F7FBFF",
                 fg="#2E4057").pack(pady=15)

        # 表格（稳定布局，数据正常显示）
        tree = ttk.Treeview(self.root, columns=("time", "name", "phone"), show="headings")
        tree.heading("time", text="就诊时间")
        tree.heading("name", text="姓名")
        tree.heading("phone", text="联系电话")
        tree.column("time", width=220, anchor=tk.CENTER)
        tree.column("name", width=140, anchor=tk.CENTER)
        tree.column("phone", width=180, anchor=tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)

        # 加载数据（确保数据正常显示）
        if not records:
            messagebox.showinfo("提示", f"暂无{type_name}病历")
        else:
            for r in records:
                tree.insert("", tk.END, values=(r.get("time"), r.get("name"), r.get("phone")))

        # 查看详情
        def view():
            sel = tree.selection()
            if sel:
                idx = tree.index(sel[0])
                self.clear_all()
                DetailWindow(self.root, records[idx], self.show_main)

        # 打印病历
        def print_item():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("提示", "请选择一条记录")
                return
            idx = tree.index(sel[0])
            r = records[idx]
            content = (
                f"============ 医疗服务系统 ============\n"
                f"姓名：{r.get('name')}    性别：{r.get('gender')}    年龄：{r.get('age')}\n"
                f"电话：{r.get('phone')}    分类：{r.get('type')}\n"
                f"时间：{r.get('time')}\n\n"
                f"【诊断】\n{r.get('diagnosis')}\n"
                f"============================================"
            )
            pw = tk.Toplevel(self.root)
            pw.title("打印病历")
            pw.geometry("700x500")
            text = tk.Text(pw, font=("微软雅黑", 12), bg="white", wrap=tk.WORD)
            text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            text.insert("end", content)
            text.config(state=tk.DISABLED)
            tk.Button(pw, text="确认打印", command=lambda: text.event_generate("<<Print>>")).pack(pady=10)

        # 按钮区
        bf = tk.Frame(self.root, bg="#F7FBFF")
        bf.pack(pady=12)
        tk.Button(bf, text="查看详情", font=("微软雅黑", 12), bg="#5AA7DE", fg="white", width=12, command=view).grid(
            row=0, column=0, padx=10)
        tk.Button(bf, text="打印病历", font=("微软雅黑", 12), bg="#5AA7DE", fg="white", width=12,
                  command=print_item).grid(row=0, column=1, padx=10)
        tk.Button(bf, text="返回主菜单", font=("微软雅黑", 12), bg="#4A90E2", fg="white", width=14,
                  command=self.show_main).grid(row=0, column=2, padx=10)

    def show_new_record(self):
        self.clear_all()
        NewRecordWindow(self.root, self.show_main)

    def show_query(self):
        self.clear_all()
        QueryWindow(self.root, self.show_main)

    def clear_all(self):
        for w in self.root.winfo_children():
            w.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MedicalApp()
    app.run()