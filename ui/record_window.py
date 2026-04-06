import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from core.data_manager import DataManager
import time
import uuid
from datetime import datetime

class NewRecordWindow:
    def __init__(self, root, back_menu):
        self.root = root
        self.back_menu = back_menu
        self.dm = DataManager()
        self.record_id = str(uuid.uuid4())  # 病历唯一ID
        self.clear_window()
        self.root.config(bg="#F7FBFF")
        self.root.title(f"新建病历 - 医疗服务系统")

        # 标题
        tk.Label(root, text="新建病历", font=("微软雅黑", 18, "bold"), bg="#F7FBFF", fg="#2E4057").pack(pady=10)

        # 主容器
        main = tk.Frame(root, bg="#F7FBFF")
        main.pack(fill=tk.BOTH, expand=True, padx=30)

        # ========== 病历信息区（文件台头） ==========
        info = tk.LabelFrame(main, text="病历基本信息", font=("微软雅黑",12,"bold"), bg="#F7FBFF", bd=1, relief=tk.SOLID)
        info.pack(fill=tk.X, pady=(0, 5))
        # 第一行：姓名、性别、年龄、分类
        row1 = tk.Frame(info, bg="#F7FBFF")
        row1.pack(fill=tk.X, pady=8, padx=15)
        tk.Label(row1, text="姓名:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=0,sticky=tk.W)
        self.name = ttk.Entry(row1, font=("微软雅黑",11), width=15)
        self.name.grid(row=0,column=1,padx=10,sticky=tk.W)
        self.name.bind("<KeyRelease>", self.sync_pres_info)  # 同步到处方笺

        tk.Label(row1, text="性别:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=2,sticky=tk.W)
        self.gender = ttk.Combobox(row1, values=["男","女"], font=("微软雅黑",11), width=8, state="readonly")
        self.gender.current(0)
        self.gender.grid(row=0,column=3,padx=10,sticky=tk.W)
        self.gender.bind("<<ComboboxSelected>>", self.sync_pres_info)  # 同步到处方笺

        tk.Label(row1, text="年龄:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=4,sticky=tk.W)
        self.age = ttk.Entry(row1, font=("微软雅黑",11), width=15)
        self.age.grid(row=0,column=5,padx=10,sticky=tk.W)
        self.age.bind("<KeyRelease>", self.sync_pres_info)  # 同步到处方笺

        tk.Label(row1, text="病历分类:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=6,sticky=tk.W)
        self.type_var = ttk.Combobox(row1, values=["中药","西药","疼痛"], font=("微软雅黑",11), width=8, state="readonly")
        self.type_var.current(0)
        self.type_var.grid(row=0,column=7,padx=10,sticky=tk.W)

        # 第二行：手机号、住址、创建时间（自动生成）
        row2 = tk.Frame(info, bg="#F7FBFF")
        row2.pack(fill=tk.X, pady=8, padx=15)
        tk.Label(row2, text="手机号:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=0,sticky=tk.W)
        self.phone = ttk.Entry(row2, font=("微软雅黑",11), width=15)
        self.phone.grid(row=0,column=1,padx=10,sticky=tk.W)

        tk.Label(row2, text="住址:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=2,sticky=tk.W)
        self.addr = ttk.Entry(row2, font=("微软雅黑",11), width=35)
        self.addr.grid(row=0,column=3,padx=10,sticky=tk.W, columnspan=4)

        tk.Label(row2, text="创建时间:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=7,sticky=tk.W)
        self.create_time = tk.Label(row2, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bg="#F7FBFF", font=("微软雅黑",11))
        self.create_time.grid(row=0,column=8,padx=10,sticky=tk.W)

        # ========== 临床诊断区（大输入框） ==========
        diag = tk.LabelFrame(main, text="临床诊断", font=("微软雅黑",12,"bold"), bg="#F7FBFF", bd=1, relief=tk.SOLID)
        diag.pack(fill=tk.BOTH, expand=True, pady=5)
        self.diag = tk.Text(diag, height=10, font=("微软雅黑",11), wrap=tk.WORD, padx=10, pady=10)
        self.diag.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ========== 处方笺区（A5格式，含门诊号） ==========
        pres_frame = tk.LabelFrame(main, text="处方笺 (可新增多个，A5打印格式)", font=("微软雅黑",12,"bold"), bg="#F7FBFF", bd=1, relief=tk.SOLID)
        pres_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 处方头部（科别、费别、日期、门诊号）
        pres_header1 = tk.Frame(pres_frame, bg="#F7FBFF")
        pres_header1.pack(fill=tk.X, pady=8, padx=15)
        tk.Label(pres_header1, text="科别:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=0,sticky=tk.W)
        self.pres_dept = ttk.Entry(pres_header1, font=("微软雅黑",11), width=15)
        self.pres_dept.grid(row=0,column=1,padx=10,sticky=tk.W)

        tk.Label(pres_header1, text="费别:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=2,sticky=tk.W)
        self.pres_fee = ttk.Combobox(pres_header1, values=["自费","医保","公费"], font=("微软雅黑",11), width=13, state="readonly")
        self.pres_fee.current(0)
        self.pres_fee.grid(row=0,column=3,padx=10,sticky=tk.W)

        tk.Label(pres_header1, text="处方日期:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=4,sticky=tk.W)
        self.pres_date = ttk.Entry(pres_header1, font=("微软雅黑",11), width=15)
        self.pres_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.pres_date.grid(row=0,column=5,padx=10,sticky=tk.W)

        tk.Label(pres_header1, text="门诊号:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=6,sticky=tk.W)
        self.pres_outpatient = tk.Label(pres_header1, text="自动生成", bg="#F7FBFF", font=("微软雅黑",11), fg="#666")
        self.pres_outpatient.grid(row=0,column=7,padx=10,sticky=tk.W)

        # 处方头部2（姓名、性别、年龄）- 自动同步
        pres_header2 = tk.Frame(pres_frame, bg="#F7FBFF")
        pres_header2.pack(fill=tk.X, pady=8, padx=15)
        tk.Label(pres_header2, text="患者姓名:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=0,sticky=tk.W)
        self.pres_name = ttk.Entry(pres_header2, font=("微软雅黑",11), width=15, state="readonly")
        self.pres_name.grid(row=0,column=1,padx=10,sticky=tk.W)

        tk.Label(pres_header2, text="患者性别:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=2,sticky=tk.W)
        self.pres_gender = ttk.Combobox(pres_header2, values=["男","女"], font=("微软雅黑",11), width=8, state="readonly")
        self.pres_gender.current(0)
        self.pres_gender.grid(row=0,column=3,padx=10,sticky=tk.W)

        tk.Label(pres_header2, text="患者年龄:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=4,sticky=tk.W)
        self.pres_age = ttk.Entry(pres_header2, font=("微软雅黑",11), width=15, state="readonly")
        self.pres_age.grid(row=0,column=5,padx=10,sticky=tk.W)

        # 处方诊断+药方（超大输入框，满足医生输入）
        pres_diag_frame = tk.LabelFrame(pres_frame, text="处方诊断 & 药方开具", font=("微软雅黑",12,"bold"), bg="#F7FBFF")
        pres_diag_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        self.pres_diag = tk.Text(pres_diag_frame, height=12, font=("微软雅黑",11), wrap=tk.WORD, padx=10, pady=10)
        self.pres_diag.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 处方底部（医师、审核、金额、调配、核对、发药）
        pres_footer = tk.Frame(pres_frame, bg="#F7FBFF")
        pres_footer.pack(fill=tk.X, pady=8, padx=15)
        tk.Label(pres_footer, text="医师:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=0,sticky=tk.W)
        self.pres_doctor = ttk.Entry(pres_footer, font=("微软雅黑",11), width=12)
        self.pres_doctor.grid(row=0,column=1,padx=8,sticky=tk.W)

        tk.Label(pres_footer, text="审核:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=2,sticky=tk.W)
        self.pres_audit = ttk.Entry(pres_footer, font=("微软雅黑",11), width=12)
        self.pres_audit.grid(row=0,column=3,padx=8,sticky=tk.W)

        tk.Label(pres_footer, text="金额(元):", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=4,sticky=tk.W)
        self.pres_amount = ttk.Entry(pres_footer, font=("微软雅黑",11), width=12)
        self.pres_amount.grid(row=0,column=5,padx=8,sticky=tk.W)

        tk.Label(pres_footer, text="调配:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=6,sticky=tk.W)
        self.pres_dispense = ttk.Entry(pres_footer, font=("微软雅黑",11), width=12)
        self.pres_dispense.grid(row=0,column=7,padx=8,sticky=tk.W)

        tk.Label(pres_footer, text="核对:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=8,sticky=tk.W)
        self.pres_check = ttk.Entry(pres_footer, font=("微软雅黑",11), width=12)
        self.pres_check.grid(row=0,column=9,padx=8,sticky=tk.W)

        tk.Label(pres_footer, text="发药:", bg="#F7FBFF", font=("微软雅黑",11), width=8).grid(row=0,column=10,sticky=tk.W)
        self.pres_dispense_med = ttk.Entry(pres_footer, font=("微软雅黑",11), width=12)
        self.pres_dispense_med.grid(row=0,column=11,padx=8,sticky=tk.W)

        # ========== 功能按钮区 ==========
        btn_f = tk.Frame(main, bg="#F7FBFF")
        btn_f.pack(pady=15)
        tk.Button(btn_f, text="保存病历", command=self.save_record, bg="#4A90E2", fg="white", width=14, font=("微软雅黑",12), bd=0).grid(row=0,column=0,padx=8)
        tk.Button(btn_f, text="新增处方笺", command=self.add_prescription, bg="#5AA7DE", fg="white", width=14, font=("微软雅黑",12), bd=0).grid(row=0,column=1,padx=8)
        tk.Button(btn_f, text="打印病历", command=self.print_record, bg="#3CB371", fg="white", width=14, font=("微软雅黑",12), bd=0).grid(row=0,column=2,padx=8)
        tk.Button(btn_f, text="打印处方笺", command=self.print_pres, bg="#FF9F43", fg="white", width=14, font=("微软雅黑",12), bd=0).grid(row=0,column=3,padx=8)
        tk.Button(btn_f, text="返回主菜单", command=self.back_menu, bg="#999999", fg="white", width=14, font=("微软雅黑",12), bd=0).grid(row=0,column=4,padx=8)

        # 初始化同步一次默认值
        self.sync_pres_info()

    # 核心功能：自动同步病历信息到处方笺
    def sync_pres_info(self, event=None):
        self.pres_name.config(state="normal")
        self.pres_name.delete(0, tk.END)
        self.pres_name.insert(0, self.name.get().strip())
        self.pres_name.config(state="readonly")

        self.pres_gender.set(self.gender.get())

        self.pres_age.config(state="normal")
        self.pres_age.delete(0, tk.END)
        self.pres_age.insert(0, self.age.get().strip())
        self.pres_age.config(state="readonly")

    # 清空窗口
    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    # 保存病历
    def save_record(self):
        # 校验必填项
        if not self.name.get().strip():
            messagebox.showwarning("提示", "请输入患者姓名！")
            return
        if not self.phone.get().strip():
            messagebox.showwarning("提示", "请输入患者手机号！")
            return
        if not self.diag.get("1.0", tk.END).strip():
            messagebox.showwarning("提示", "请填写临床诊断！")
            return

        # 构造病历数据
        record_data = {
            "id": self.record_id,
            "name": self.name.get().strip(),
            "gender": self.gender.get(),
            "age": self.age.get().strip(),
            "phone": self.phone.get().strip(),
            "address": self.addr.get().strip(),
            "type": self.type_var.get(),
            "diagnosis": self.diag.get("1.0", tk.END).strip(),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # 保存病历
        self.dm.add_record(record_data)
        # 保存当前处方笺
        self.add_prescription(save_only=True)
        messagebox.showinfo("保存成功", "病历及处方笺已成功保存！")
        self.back_menu()

    # 新增处方笺（支持仅保存不弹窗）
    def add_prescription(self, save_only=False):
        if not self.name.get().strip():
            messagebox.showwarning("提示", "请先填写患者基本信息！")
            return
        # 构造处方数据
        pres_data = {
            "record_id": self.record_id,
            "dept": self.pres_dept.get().strip(),
            "fee": self.pres_fee.get(),
            "date": self.pres_date.get().strip(),
            "name": self.pres_name.get().strip(),
            "gender": self.pres_gender.get(),
            "age": self.pres_age.get().strip(),
            "diagnosis": self.pres_diag.get("1.0", tk.END).strip(),
            "doctor": self.pres_doctor.get().strip(),
            "audit": self.pres_audit.get().strip(),
            "amount": self.pres_amount.get().strip(),
            "dispense": self.pres_dispense.get().strip(),
            "check": self.pres_check.get().strip(),
            "dispense_med": self.pres_dispense_med.get().strip(),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # 保存处方
        self.dm.add_prescription(pres_data)
        if not save_only:
            messagebox.showinfo("新增成功", "处方笺已新增并保存！")
            # 清空处方框（保留患者信息）
            self.pres_dept.delete(0, tk.END)
            self.pres_fee.current(0)
            self.pres_date.delete(0, tk.END)
            self.pres_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.pres_diag.delete("1.0", tk.END)
            self.pres_doctor.delete(0, tk.END)
            self.pres_audit.delete(0, tk.END)
            self.pres_amount.delete(0, tk.END)
            self.pres_dispense.delete(0, tk.END)
            self.pres_check.delete(0, tk.END)
            self.pres_dispense_med.delete(0, tk.END)

    # 打印病历（支持打印机+PDF）
    def print_record(self):
        if not self.name.get().strip():
            messagebox.showwarning("提示", "请先填写病历信息！")
            return
        # 构造打印内容
        content = f"""==================== 医疗服务系统 - 病历单 ====================
病历编号：{self.record_id}
患者姓名：{self.name.get().strip()}        性别：{self.gender.get()}        年龄：{self.age.get().strip()}
联系电话：{self.phone.get().strip()}        住址：{self.addr.get().strip() or "未填写"}
病历分类：{self.type_var.get()}        创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

==================== 临床诊断 ====================
{self.diag.get("1.0", tk.END).strip() or "未填写"}

=================================================
打印时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        # 打印窗口
        win = Toplevel(self.root)
        win.title("打印病历 - 医疗服务系统")
        win.geometry("800x700")
        win.resizable(True, True)
        # 文本框展示
        text = tk.Text(win, font=("微软雅黑", 12), wrap=tk.WORD, bg="white", padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text.insert("end", content)
        text.config(state=tk.DISABLED)
        # 打印按钮
        btn_frame = tk.Frame(win, bg="#f8f9fa")
        btn_frame.pack(fill=tk.X, pady=10)
        tk.Button(btn_frame, text="打印机打印", command=lambda: text.event_generate("<<Print>>"), bg="#3498db", fg="white", font=("微软雅黑",12), width=15).pack(side=tk.LEFT, padx=20)
        tk.Button(btn_frame, text="保存为PDF", command=lambda: self.save_as_pdf(content, "病历单"), bg="#e67e22", fg="white", font=("微软雅黑",12), width=15).pack(side=tk.RIGHT, padx=20)

    # 打印处方笺（A5格式，支持打印机+PDF）
    def print_pres(self):
        if not self.name.get().strip():
            messagebox.showwarning("提示", "请先填写处方信息！")
            return
        # 构造A5格式处方内容
        content = f"""科别：{self.pres_dept.get().strip() or "未填写"}        费别：{self.pres_fee.get()}        日期：{self.pres_date.get().strip()}
门诊号：{self.pres_outpatient["text"] if self.pres_outpatient["text"] != "自动生成" else "待生成"}        姓名：{self.pres_name.get().strip()}
性别：{self.pres_gender.get()}        年龄：{self.pres_age.get().strip() or "未填写"}

【处方诊断 & 药方】
{self.pres_diag.get("1.0", tk.END).strip() or "未填写"}

医师：{self.pres_doctor.get().strip() or "未填写"}        审核：{self.pres_audit.get().strip() or "未填写"}        金额：{self.pres_amount.get().strip() or "0.00"} 元
调配：{self.pres_dispense.get().strip() or "未填写"}        核对：{self.pres_check.get().strip() or "未填写"}        发药：{self.pres_dispense_med.get().strip() or "未填写"}

打印时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        # A5打印窗口（420x594像素，适配A5纸）
        win = Toplevel(self.root)
        win.title("打印处方笺(A5) - 医疗服务系统")
        win.geometry("420x594")
        win.resizable(False, False)  # 固定A5尺寸
        # 文本框展示（宋体，适配处方打印）
        text = tk.Text(win, font=("宋体", 12), wrap=tk.WORD, bg="white", padx=15, pady=15)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert("end", content)
        text.config(state=tk.DISABLED)
        # 打印按钮
        btn_frame = tk.Frame(win, bg="#f8f9fa")
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="A5打印机打印", command=lambda: text.event_generate("<<Print>>"), bg="#3498db", fg="white", font=("微软雅黑",11), width=12).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="保存为PDF", command=lambda: self.save_as_pdf(content, "处方笺"), bg="#e67e22", fg="white", font=("微软雅黑",11), width=12).pack(side=tk.RIGHT, padx=15)

    # 保存为PDF（需安装reportlab，兼容PyCharm）
    def save_as_pdf(self, content, file_name):
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4, A5
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.cmaps import gb2312
            from reportlab.pdfbase.ttfonts import TTFont
            import os

            # 注册中文字体（解决PDF中文乱码，需确保有微软雅黑字体）
            pdfmetrics.registerFont(TTFont("MSYH", "msyh.ttc"))
            pdfmetrics.registerFontMapping("GB2312", "MSYH")

            # 生成保存路径
            save_dir = "print_pdf"
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, f"{file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")

            # 创建PDF（处方笺用A5，病历用A4）
            pagesize = A5 if file_name == "处方笺" else A4
            c = canvas.Canvas(file_path, pagesize=pagesize)
            c.setFont("MSYH", 10 if file_name == "处方笺" else 12)

            # 写入内容（按行分割）
            lines = content.split("\n")
            y = pagesize[1] - 20  # 起始y坐标
            line_height = 15 if file_name == "处方笺" else 18
            for line in lines:
                c.drawString(20, y, line)
                y -= line_height
                if y < 20:  # 分页
                    c.showPage()
                    c.setFont("MSYH", 10 if file_name == "处方笺" else 12)
                    y = pagesize[1] - 20

            # 保存PDF
            c.save()
            messagebox.showinfo("PDF保存成功", f"已保存至：{file_path}")
        except ImportError:
            messagebox.showwarning("依赖缺失", "请先安装reportlab：pip install reportlab")
        except Exception as e:
            messagebox.showerror("保存失败", f"PDF保存失败：{str(e)}")