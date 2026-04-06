import tkinter as tk
from tkinter import ttk, messagebox
from core.data_manager import DataManager
from datetime import datetime


class QueryWindow:
    def __init__(self, root, back_func):
        self.root = root
        self.back_func = back_func
        self.dm = DataManager()
        self.selected_record = None
        self.tree = None
        self.clear_window()
        self.root.config(bg="#f0f4f8")
        self.root.title("历史病历查询 - 医疗服务系统")

        # ===================== 1. 标题区域（统一风格） =====================
        tk.Label(root, text="历史病历查询", font=("微软雅黑", 18, "bold"),
                 bg="#f0f4f8", fg="#1a237e").pack(pady=15)

        # ===================== 2. 搜索区域（排版优化+高对比度） =====================
        search_frame = tk.Frame(root, bg="#f0f4f8")
        search_frame.pack(fill=tk.X, pady=10, padx=30)

        # 全局按钮统一样式（高对比度，字体绝对清晰）
        self.btn_style = {
            "font": ("微软雅黑", 11, "bold"),
            "bg": "#2196F3",  # 专业医疗蓝
            "fg": "white",  # 纯白字体，不受系统主题影响
            "activebackground": "#1976D2",  # 鼠标悬浮加深
            "activeforeground": "white",
            "bd": 0,
            "relief": tk.FLAT,
            "padx": 12,
            "pady": 6
        }

        # 搜索标签（对齐优化，宽度固定）
        tk.Label(search_frame, text="搜索（姓名/手机号）：",
                 bg="#f0f4f8", font=("微软雅黑", 11, "bold"), fg="#1a237e",
                 width=18, anchor=tk.W).grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)

        # 搜索输入框（样式优化，边框清晰）
        self.search_entry = ttk.Entry(search_frame, font=("微软雅黑", 11), width=35)
        self.search_entry.grid(row=0, column=1, padx=5, pady=8, sticky=tk.W)

        # 搜索按钮（排版对齐，高对比度）
        tk.Button(search_frame, text="立即查询", command=self.search_records, **self.btn_style) \
            .grid(row=0, column=2, padx=8, pady=8)
        tk.Button(search_frame, text="显示全部", command=self.load_all_records, **self.btn_style) \
            .grid(row=0, column=3, padx=5, pady=8)

        # 绑定回车查询
        self.search_entry.bind("<Return>", lambda e: self.search_records())

        # ===================== 3. 表格区域（表头颜色优化+排版整齐） =====================
        table_frame = tk.Frame(root, bg="#f0f4f8", bd=1, relief=tk.SOLID)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=30)

        # 表格列定义
        self.columns = ("name", "gender", "phone", "type", "time")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=15)

        # 表头样式（深蓝背景+白字，清晰醒目）
        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            font=("微软雅黑", 10, "bold"),
            background="#2196F3",
            foreground="white",
            relief=tk.FLAT
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#1976D2")],
            foreground=[("active", "white")]
        )
        # 表格内容样式（行高优化，阅读舒适）
        style.configure(
            "Treeview",
            font=("微软雅黑", 10),
            background="white",
            foreground="#1a237e",
            rowheight=25
        )

        # 表头配置+列宽（排版整齐）
        self.tree.heading("name", text="患者姓名")
        self.tree.heading("gender", text="性别")
        self.tree.heading("phone", text="联系电话")
        self.tree.heading("type", text="病历分类")
        self.tree.heading("time", text="就诊时间")

        self.tree.column("name", width=140, anchor=tk.CENTER)
        self.tree.column("gender", width=80, anchor=tk.CENTER)
        self.tree.column("phone", width=180, anchor=tk.CENTER)
        self.tree.column("type", width=100, anchor=tk.CENTER)
        self.tree.column("time", width=220, anchor=tk.CENTER)

        # 滚动条
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ===================== 4. 底部功能按钮（高对比度+排版整齐） =====================
        btn_frame = tk.Frame(root, bg="#f0f4f8")
        btn_frame.pack(fill=tk.X, pady=15, padx=30)

        # 按钮样式分类（功能区分，颜色明确）
        detail_btn_style = {**self.btn_style, "width": 14}
        del_btn_style = {
            **self.btn_style,
            "bg": "#f44336",  # 警示红（删除按钮）
            "activebackground": "#d32f2f",
            "width": 14
        }
        back_btn_style = {
            **self.btn_style,
            "bg": "#95a5a6",  # 中性灰（返回按钮）
            "activebackground": "#7f8c8d",
            "width": 14
        }

        # 功能按钮（排版对齐，字体清晰）
        self.detail_btn = tk.Button(btn_frame, text="查看/编辑详情", command=self.view_detail,
                                    state=tk.DISABLED, **detail_btn_style)
        self.detail_btn.pack(side=tk.LEFT, padx=8)

        self.del_btn = tk.Button(btn_frame, text="删除选中病历", command=self.delete_selected,
                                 state=tk.DISABLED, **del_btn_style)
        self.del_btn.pack(side=tk.LEFT, padx=8)

        tk.Button(btn_frame, text="返回主菜单", command=self.back_func, **back_btn_style) \
            .pack(side=tk.RIGHT, padx=8)

        # 初始加载所有病历
        self.load_all_records()

    # ===================== 工具方法（保持功能+安全修复） =====================
    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.tree = None

    # 核心修复：安全加载数据，避免控件销毁报错
    def load_all_records(self):
        # 【终极修复】如果tree已经不存在，直接重建整个界面
        if not hasattr(self, 'tree') or not self.tree or not self.tree.winfo_exists():
            self.show_main()
            return

        # 安全清空旧数据
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
        except:
            pass

        # 加载数据
        self.dm.load_records()
        self.dm.load_prescriptions()

        sorted_records = sorted(self.dm.records, key=lambda x: x.get("time", ""), reverse=True)

        for record in sorted_records:
            self.tree.insert("", tk.END, values=(
                record.get("name", ""),
                record.get("gender", ""),
                record.get("phone", ""),
                record.get("type", ""),
                record.get("time", "")
            ))

        self.selected_record = None
        self.detail_btn.config(state=tk.DISABLED)
        self.del_btn.config(state=tk.DISABLED)

    def show_main(self):
        """返回时重建整个查询界面，彻底解决空白/报错"""
        self.clear_window()
        self.__init__(self.root, self.back_func)

    # 搜索功能（排版优化后功能不变）
    def search_records(self):
        if not self.tree or not self.tree.winfo_exists():
            # 直接return会导致搜索后空白，改成跳过删除
            pass
        else:
            for item in self.tree.get_children():
                self.tree.delete(item)
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("提示", "请输入姓名或手机号进行搜索！")
            return
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 模糊筛选
        filtered = [r for r in self.dm.records if keyword in r.get("name", "") or keyword in r.get("phone", "")]
        # 倒序排序
        filtered_sorted = sorted(filtered, key=lambda x: x.get("time", ""), reverse=True)
        # 填充表格
        for record in filtered_sorted:
            self.tree.insert("", tk.END, values=(
                record.get("name", ""),
                record.get("gender", ""),
                record.get("phone", ""),
                record.get("type", ""),
                record.get("time", "")
            ))
        # 重置选中状态
        self.selected_record = None
        self.detail_btn.config(state=tk.DISABLED)
        self.del_btn.config(state=tk.DISABLED)
        if not filtered_sorted:
            messagebox.showinfo("提示", f"未找到包含【{keyword}】的病历！")

    # 表格选中事件（安全判断）
    def on_select(self, event):
        if not self.tree or not self.tree.winfo_exists():
            return
        selected = self.tree.selection()
        if not selected:
            self.selected_record = None
            self.detail_btn.config(state=tk.DISABLED)
            self.del_btn.config(state=tk.DISABLED)
            return
        # 获取选中行数据
        item = selected[0]
        values = self.tree.item(item, "values")
        # 匹配完整病历数据
        for record in self.dm.records:
            if record.get("name") == values[0] and record.get("phone") == values[2] and record.get("time") == values[4]:
                self.selected_record = record
                self.detail_btn.config(state=tk.NORMAL)
                self.del_btn.config(state=tk.NORMAL)
                break

    # 查看详情（功能不变）
    def view_detail(self):
        if not self.selected_record:
            messagebox.showwarning("提示", "请先选中一条病历！")
            return
        from ui.detail_window import DetailWindow
        DetailWindow(self.root, self.selected_record, self.load_all_records)

    # 删除病历（功能不变）
    def delete_selected(self):
        if not self.selected_record:
            messagebox.showwarning("提示", "请先选中一条病历！")
            return
        name = self.selected_record.get("name", "患者")
        if not messagebox.askyesno("确认删除", f"确定删除【{name}】的病历及所有处方笺吗？\n删除后无法恢复！"):
            return
        try:
            self.dm.delete_record_and_pres(self.selected_record.get("id", ""))
            messagebox.showinfo("删除成功", "病历及关联处方笺已删除！")
            self.load_all_records()
        except Exception as e:
            messagebox.showerror("删除失败", f"病历删除失败：{str(e)}")