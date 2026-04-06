import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from core.data_manager import DataManager
import time
from datetime import datetime
import os

class DetailWindow:
    # 安全清空窗口控件
    def clear_window(self):
        try:
            for widget in self.root.winfo_children():
                widget.destroy()
        except Exception:
            pass

    # 【核心修复】安全返回主菜单，不卡死、不空白
    def _go_to_main(self):
        self.clear_window()
        # 延迟执行主菜单回调，彻底解决Tkinter渲染冲突
        self.root.after(10, self.back_func)

    # 切换处方笺
    def switch_prescription(self, event):
        self.current_pres_idx = self.pres_sel.current()
        self.current_pres = self.prescriptions[self.current_pres_idx]
        self.__init__(self.root, self.record, self.back_func)

    # 独立编辑按钮：解锁所有输入框
    def edit_data(self):
        # 解锁病历信息
        self.name.config(state="normal")
        self.gender.config(state="normal")
        self.age.config(state="normal")
        # 新增：解锁病历分类
        self.type.config(state="normal")
        self.phone.config(state="normal")
        self.addr.config(state="normal")
        # 新增：创建时间只读，不解锁
        self.create_time.config(state="readonly")
        self.diag_text.config(state=tk.NORMAL)
        # 解锁处方信息（含大文本框）
        self.pres_name.config(state="normal")
        self.pres_gender.config(state="normal")
        self.pres_age.config(state="normal")
        self.pres_dept.config(state="normal")
        self.pres_fee.config(state="normal")
        self.pres_date.config(state="normal")
        self.pres_diag_text.config(state=tk.NORMAL)
        self.pres_doctor.config(state="normal")
        self.pres_audit.config(state="normal")
        self.pres_amount.config(state="normal")
        self.pres_dispense.config(state="normal")
        self.pres_check.config(state="normal")
        self.pres_drug.config(state="normal")
        # 编辑时禁用危险按钮
        self.add_pres_btn.config(state=tk.DISABLED)
        self.print_record_btn.config(state=tk.DISABLED)
        self.print_pres_btn.config(state=tk.DISABLED)
        self.del_btn.config(state=tk.DISABLED)
        messagebox.showinfo("提示", "已进入编辑模式，可修改病历和处方信息！")

    # 独立保存按钮：保存并锁定输入框
    def save_data(self):
        try:
            # 保存病历数据（新增type字段）
            updated_record = {
                "id": self.record_id,
                "name": self.name.get().strip(),
                "gender": self.gender.get(),
                "age": self.age.get().strip(),
                # 新增：病历分类
                "type": self.type.get(),
                "phone": self.phone.get().strip(),
                "address": self.addr.get().strip(),
                "diagnosis": self.diag_text.get("1.0", tk.END).strip(),
                "time": self.record.get("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
            # 保存处方数据（兼容新旧字段）
            pres_diag_val = self.pres_diag_text.get("1.0", tk.END).strip()
            updated_pres = {
                "id": self.current_pres.get("id", str(time.time())),
                "record_id": self.record_id,
                "name": self.pres_name.get().strip(),
                "gender": self.pres_gender.get(),
                "age": self.pres_age.get().strip(),
                "dept": self.pres_dept.get().strip(),
                "fee": self.pres_fee.get(),
                "date": self.pres_date.get().strip(),
                "pres_diagnosis": pres_diag_val,
                "diagnosis": pres_diag_val,
                "doctor": self.pres_doctor.get().strip(),
                "audit": self.pres_audit.get().strip(),
                "amount": self.pres_amount.get().strip(),
                "dispense": self.pres_dispense.get().strip(),
                "check": self.pres_check.get().strip(),
                "drug": self.pres_drug.get().strip(),
                "dispense_med": self.pres_drug.get().strip(),
                "time": self.current_pres.get("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
            self.dm.update_record(updated_record)
            self.dm.update_prescription(updated_pres)
            self.record = updated_record
            self.prescriptions[self.current_pres_idx] = updated_pres
            # 锁定所有输入框
            self.name.config(state="readonly")
            self.gender.config(state="readonly")
            self.age.config(state="readonly")
            # 新增：锁定病历分类
            self.type.config(state="readonly")
            self.phone.config(state="readonly")
            self.addr.config(state="readonly")
            # 新增：创建时间保持只读
            self.create_time.config(state="readonly")
            self.diag_text.config(state=tk.DISABLED)
            self.pres_name.config(state="readonly")
            self.pres_gender.config(state="readonly")
            self.pres_age.config(state="readonly")
            self.pres_dept.config(state="readonly")
            self.pres_fee.config(state="readonly")
            self.pres_date.config(state="readonly")
            self.pres_diag_text.config(state=tk.DISABLED)
            self.pres_doctor.config(state="readonly")
            self.pres_audit.config(state="readonly")
            self.pres_amount.config(state="readonly")
            self.pres_dispense.config(state="readonly")
            self.pres_check.config(state="readonly")
            self.pres_drug.config(state="readonly")
            # 恢复按钮
            self.add_pres_btn.config(state=tk.NORMAL)
            self.print_record_btn.config(state=tk.NORMAL)
            self.print_pres_btn.config(state=tk.NORMAL)
            self.del_btn.config(state=tk.NORMAL)
            messagebox.showinfo("成功", "病历和处方信息已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")

    # 新增处方笺
    def add_prescription(self):
        try:
            new_pres = {
                "id": str(time.time()),
                "record_id": self.record_id,
                "name": self.record.get("name", ""),
                "gender": self.record.get("gender", "男"),
                "age": self.record.get("age", ""),
                "dept": "",
                "fee": "自费",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "pres_diagnosis": "",
                "diagnosis": "",
                "doctor": "",
                "audit": "",
                "amount": "",
                "dispense": "",
                "check": "",
                "drug": "",
                "dispense_med": "",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.dm.add_prescription(new_pres)
            messagebox.showinfo("成功", "新增处方成功！")
            self.__init__(self.root, self.record, self.back_func)
        except Exception as e:
            messagebox.showerror("错误", f"新增失败：{str(e)}")

    # 打印病历
    # ===================== 【最终版】打印病历：标题居中 + 内容左对齐 =====================
    def print_record(self):
        try:
            import win32print
            import win32ui
            import win32con
            from datetime import datetime

            content = f"""
=====================================================================================================================================
                           病历详情
=====================================================================================================================================

病历编号：{self.record_id}
姓    名：{self.record.get('name', '')}
性    别：{self.record.get('gender', '')}
年    龄：{self.record.get('age', '')}
病历分类：{self.record.get('type', '中药')}
创建时间：{self.record.get('time', '')}
电    话：{self.record.get('phone', '')}
地    址：{self.record.get('address', '')}

诊断内容：
{self.record.get('diagnosis', '无诊断信息')}

=====================================================================================================================================
                            打印时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
    """

            hprinter = win32print.GetDefaultPrinter()
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(hprinter)
            hdc.SetMapMode(win32con.MM_LOMETRIC)

            hdc.StartDoc("病历打印")
            hdc.StartPage()

            # 大字体
            font = win32ui.CreateFont({
                "name": "宋体",
                "height": -42,
                "weight": 400,
            })
            hdc.SelectObject(font)

            # 打印：标题居中，内容左对齐
            y = -80
            lines = content.strip().split("\n")

            for line in lines:
                if "=====" in line or "病历详情" in line or "打印时间" in line:
                    # 标题、边框、打印时间 → 居中
                    text_width = len(line) * 22
                    x = (1480 - text_width) // 2
                    hdc.TextOut(x, y, line)
                else:
                    # 内容 → 左对齐
                    hdc.TextOut(100, y, line)

                y -= 48

            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()

            messagebox.showinfo("打印成功", "已发送至打印机！")
        except Exception as e:
            messagebox.showerror("打印失败", f"错误：{str(e)}")

    # ===================== 【最终版】打印处方：标题居中 + 内容左对齐 =====================
    def print_pres(self):
        try:
            import win32print
            import win32ui
            import win32con
            from datetime import datetime

            content = f"""
=====================================================================================================================================
                            处方笺
=====================================================================================================================================

病历编号：{self.current_pres.get('record_id', '')}
患者姓名：{self.current_pres.get('name', '')}
患者性别：{self.current_pres.get('gender', '')}
患者年龄：{self.current_pres.get('age', '')}
科    室：{self.current_pres.get('dept', '')}
费    别：{self.current_pres.get('fee', '')}
日    期：{self.current_pres.get('date', '')}
医    师：{self.current_pres.get('doctor', '')}
审    核：{self.current_pres.get('audit', '')}
金    额：{self.current_pres.get('amount', '')} 元
调    配：{self.current_pres.get('dispense', '')}
核    对：{self.current_pres.get('check', '')}
发    药：{self.current_pres.get('drug', '')}

处方诊断 & 药方：
{self.current_pres.get('pres_diagnosis', self.current_pres.get('diagnosis', '无处方信息'))}

=====================================================================================================================================
                            打印时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
    """

            hprinter = win32print.GetDefaultPrinter()
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(hprinter)
            hdc.SetMapMode(win32con.MM_LOMETRIC)

            hdc.StartDoc("处方打印")
            hdc.StartPage()

            font = win32ui.CreateFont({
                "name": "宋体",
                "height": -42,
                "weight": 400,
            })
            hdc.SelectObject(font)

            y = -80
            lines = content.strip().split("\n")

            for line in lines:
                if "=====" in line or "处方笺" in line or "打印时间" in line:
                    # 标题、边框、打印时间 → 居中
                    text_width = len(line) * 22
                    x = (1480 - text_width) // 2
                    hdc.TextOut(x, y, line)
                else:
                    # 内容 → 左对齐
                    hdc.TextOut(100, y, line)

                y -= 48

            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()

            messagebox.showinfo("打印成功", "已发送至打印机！")
        except Exception as e:
            messagebox.showerror("打印失败", f"错误：{str(e)}")

    # 删除病历
    def delete_record(self):
        if not messagebox.askyesno("确认", "确定删除该病历及所有处方？删除后无法恢复！"):
            return
        try:
            self.dm.delete_record_and_pres(self.record_id)
            messagebox.showinfo("成功", "病历删除成功！")
            self._go_to_main()
        except Exception as e:
            messagebox.showerror("错误", f"删除失败：{str(e)}")

    # 构造函数：【新增字段】病历分类+创建时间，布局完全匹配需求
    def __init__(self, root, record, back_func):
        self.root = root
        self.record = record
        self.back_func = back_func
        self.dm = DataManager()
        self.record_id = record.get("id", "")
        self.current_pres_idx = 0

        # 加载历史处方数据
        self.dm.load_prescriptions()
        self.prescriptions = self.dm.get_prescriptions_by_record_id(self.record_id)
        if not self.prescriptions:
            self.prescriptions = [{
                "id": str(time.time()),
                "record_id": self.record_id,
                "name": record.get("name", ""),
                "gender": record.get("gender", "男"),
                "age": record.get("age", ""),
                "dept": "",
                "fee": "自费",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "pres_diagnosis": "",
                "diagnosis": "",
                "doctor": "",
                "audit": "",
                "amount": "",
                "dispense": "",
                "check": "",
                "drug": "",
                "dispense_med": "",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }]
        self.current_pres = self.prescriptions[self.current_pres_idx]

        # 初始化界面
        self.clear_window()
        self.root.config(bg="#f0f4f8")
        self.root.title(f"历史病历详情 - {record.get('name')}")

        # 按钮样式（完全匹配参考图）
        self.btn_style = {"font": ("微软雅黑", 10, "bold"), "fg": "white", "bd": 0, "relief": tk.FLAT, "padx": 15, "pady": 6}
        self.edit_style = {**self.btn_style, "bg": "#2196F3"}      # 编辑：蓝色
        self.save_style = {**self.btn_style, "bg": "#4CAF50"}      # 保存：绿色
        self.add_style = {**self.btn_style, "bg": "#2196F3"}       # 新增处方：蓝色
        self.print_style = {**self.btn_style, "bg": "#FF9800"}     # 打印：橙色
        self.del_style = {**self.btn_style, "bg": "#f44336"}       # 删除：红色
        self.back_style = {**self.btn_style, "bg": "#95a5a6"}      # 返回：灰色

        # ===================== 标题栏 =====================
        title_label = tk.Label(root, text="历史病历详情", font=("微软雅黑", 18, "bold"), bg="#f0f4f8", fg="#1a237e")
        title_label.pack(anchor=tk.W, padx=10, pady=10)

        # ===================== 【修改完成】患者病历信息面板 =====================
        record_frame = tk.LabelFrame(root, text="患者病历信息", font=("微软雅黑", 11, "bold"), bg="#f0f4f8", padx=10, pady=10)
        record_frame.pack(fill=tk.X, padx=10, pady=5)

        # 第一行：姓名、性别、年龄、【新增】病历分类
        row1 = tk.Frame(record_frame, bg="#f0f4f8")
        row1.pack(fill=tk.X, pady=3)
        tk.Label(row1, text="姓名：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.name = ttk.Entry(row1, font=("微软雅黑", 10), width=12)
        self.name.insert(0, record.get("name", ""))
        self.name.config(state="readonly")
        self.name.pack(side=tk.LEFT, padx=5)

        tk.Label(row1, text="性别：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.gender = ttk.Combobox(row1, values=["男", "女"], state="readonly", font=("微软雅黑", 10), width=8)
        self.gender.set(record.get("gender", "男"))
        self.gender.pack(side=tk.LEFT, padx=5)

        tk.Label(row1, text="年龄：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.age = ttk.Entry(row1, font=("微软雅黑", 10), width=8)
        self.age.insert(0, record.get("age", ""))
        self.age.config(state="readonly")
        self.age.pack(side=tk.LEFT, padx=5)

        # 【新增】病历分类（显示中药/西药等）
        tk.Label(row1, text="病历分类：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.type = ttk.Combobox(row1, values=["中药", "西药", "疼痛"], state="readonly", font=("微软雅黑", 10), width=8)
        self.type.set(record.get("type", "中药"))
        self.type.config(state="readonly")
        self.type.pack(side=tk.LEFT, padx=5)

        # 第二行：电话、地址、【新增】病历创建时间
        row2 = tk.Frame(record_frame, bg="#f0f4f8")
        row2.pack(fill=tk.X, pady=3)
        tk.Label(row2, text="电话：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.phone = ttk.Entry(row2, font=("微软雅黑", 10), width=15)
        self.phone.insert(0, record.get("phone", ""))
        self.phone.config(state="readonly")
        self.phone.pack(side=tk.LEFT, padx=5)

        tk.Label(row2, text="地址：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.addr = ttk.Entry(row2, font=("微软雅黑", 10), width=20)
        self.addr.insert(0, record.get("address", ""))
        self.addr.config(state="readonly")
        self.addr.pack(side=tk.LEFT, padx=5)

        # 【新增】病历创建时间（只读，显示创建日期）
        tk.Label(row2, text="创建时间：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.create_time = ttk.Entry(row2, font=("微软雅黑", 10), width=20)
        # 提取时间中的日期部分，格式：2026-04-03
        create_time_str = record.get("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        create_date = create_time_str.split(" ")[0] if " " in create_time_str else create_time_str
        self.create_time.insert(0, create_date)
        self.create_time.config(state="readonly")
        self.create_time.pack(side=tk.LEFT, padx=5)

        # 第三行：诊断（大文本框）
        row3 = tk.Frame(record_frame, bg="#f0f4f8")
        row3.pack(fill=tk.X, pady=3)
        tk.Label(row3, text="诊断：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, anchor=tk.N, padx=2)
        self.diag_text = tk.Text(row3, font=("微软雅黑", 10), width=60, height=4)
        self.diag_text.insert(1.0, record.get("diagnosis", ""))
        self.diag_text.config(state=tk.DISABLED)
        self.diag_text.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # ===================== 处方信息面板 =====================
        pres_frame = tk.LabelFrame(root, text="处方信息", font=("微软雅黑", 11, "bold"), bg="#f0f4f8", padx=10, pady=10)
        pres_frame.pack(fill=tk.X, padx=10, pady=5)

        # 第一行：科室、费用、日期
        p_row1 = tk.Frame(pres_frame, bg="#f0f4f8")
        p_row1.pack(fill=tk.X, pady=3)
        tk.Label(p_row1, text="科室：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_dept = ttk.Entry(p_row1, font=("微软雅黑", 10), width=12)
        self.pres_dept.insert(0, self.current_pres.get("dept", ""))
        self.pres_dept.config(state="readonly")
        self.pres_dept.pack(side=tk.LEFT, padx=5)

        tk.Label(p_row1, text="费用：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_fee = ttk.Combobox(p_row1, values=["自费", "医保"], state="readonly", font=("微软雅黑", 10), width=8)
        self.pres_fee.set(self.current_pres.get("fee", "自费"))
        self.pres_fee.pack(side=tk.LEFT, padx=5)

        tk.Label(p_row1, text="日期：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_date = ttk.Entry(p_row1, font=("微软雅黑", 10), width=12)
        self.pres_date.insert(0, self.current_pres.get("date", datetime.now().strftime("%Y-%m-%d")))
        self.pres_date.config(state="readonly")
        self.pres_date.pack(side=tk.LEFT, padx=5)

        # 第二行：患者姓名、性别、年龄
        p_row2 = tk.Frame(pres_frame, bg="#f0f4f8")
        p_row2.pack(fill=tk.X, pady=3)
        tk.Label(p_row2, text="患者姓名：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_name = ttk.Entry(p_row2, font=("微软雅黑", 10), width=12)
        self.pres_name.insert(0, self.current_pres.get("name", record.get("name", "")))
        self.pres_name.config(state="readonly")
        self.pres_name.pack(side=tk.LEFT, padx=5)

        tk.Label(p_row2, text="患者性别：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_gender = ttk.Combobox(p_row2, values=["男", "女"], state="readonly", font=("微软雅黑", 10), width=8)
        self.pres_gender.set(self.current_pres.get("gender", record.get("gender", "男")))
        self.pres_gender.pack(side=tk.LEFT, padx=5)

        tk.Label(p_row2, text="患者年龄：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_age = ttk.Entry(p_row2, font=("微软雅黑", 10), width=8)
        self.pres_age.insert(0, self.current_pres.get("age", record.get("age", "")))
        self.pres_age.config(state="readonly")
        self.pres_age.pack(side=tk.LEFT, padx=5)

        # 第三行：处方诊断&药方开具（大文本框）
        p_row3 = tk.Frame(pres_frame, bg="#f0f4f8")
        p_row3.pack(fill=tk.X, pady=3)
        tk.Label(p_row3, text="处方诊断&药方开具：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, anchor=tk.N, padx=2)
        self.pres_diag_text = tk.Text(p_row3, font=("微软雅黑", 10), width=60, height=8)
        old_data = self.current_pres.get("diagnosis", "")
        new_data = self.current_pres.get("pres_diagnosis", "")
        fill_data = old_data if old_data else new_data
        self.pres_diag_text.insert("1.0", fill_data)
        self.pres_diag_text.config(state=tk.DISABLED)
        self.pres_diag_text.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # 第四行：医师、审核、金额
        p_row4 = tk.Frame(pres_frame, bg="#f0f4f8")
        p_row4.pack(fill=tk.X, pady=3)
        tk.Label(p_row4, text="医师：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_doctor = ttk.Entry(p_row4, font=("微软雅黑", 10), width=12)
        self.pres_doctor.insert(0, self.current_pres.get("doctor", ""))
        self.pres_doctor.config(state="readonly")
        self.pres_doctor.pack(side=tk.LEFT, padx=5)

        tk.Label(p_row4, text="审核：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_audit = ttk.Entry(p_row4, font=("微软雅黑", 10), width=12)
        self.pres_audit.insert(0, self.current_pres.get("audit", ""))
        self.pres_audit.config(state="readonly")
        self.pres_audit.pack(side=tk.LEFT, padx=5)

        tk.Label(p_row4, text="金额(元)：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_amount = ttk.Entry(p_row4, font=("微软雅黑", 10), width=12)
        self.pres_amount.insert(0, self.current_pres.get("amount", ""))
        self.pres_amount.config(state="readonly")
        self.pres_amount.pack(side=tk.LEFT, padx=5)

        # 第五行：调配、核对、发药
        p_row5 = tk.Frame(pres_frame, bg="#f0f4f8")
        p_row5.pack(fill=tk.X, pady=3)
        tk.Label(p_row5, text="调配：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_dispense = ttk.Entry(p_row5, font=("微软雅黑", 10), width=12)
        self.pres_dispense.insert(0, self.current_pres.get("dispense", ""))
        self.pres_dispense.config(state="readonly")
        self.pres_dispense.pack(side=tk.LEFT, padx=5)

        tk.Label(p_row5, text="核对：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_check = ttk.Entry(p_row5, font=("微软雅黑", 10), width=12)
        self.pres_check.insert(0, self.current_pres.get("check", ""))
        self.pres_check.config(state="readonly")
        self.pres_check.pack(side=tk.LEFT, padx=5)

        tk.Label(p_row5, text="发药：", bg="#f0f4f8", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=2)
        self.pres_drug = ttk.Entry(p_row5, font=("微软雅黑", 10), width=12)
        self.pres_drug.insert(0, self.current_pres.get("drug", self.current_pres.get("dispense_med", "")))
        self.pres_drug.config(state="readonly")
        self.pres_drug.pack(side=tk.LEFT, padx=5)

        # ===================== 功能按钮区 =====================
        btn_frame = tk.Frame(root, bg="#f0f4f8")
        btn_frame.pack(pady=15, padx=10)

        # 按钮顺序、颜色、文字完全匹配参考图
        tk.Button(btn_frame, text="编辑", command=self.edit_data, **self.edit_style).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="保存", command=self.save_data, **self.save_style).grid(row=0, column=1, padx=5)
        self.add_pres_btn = tk.Button(btn_frame, text="新增处方", command=self.add_prescription, **self.add_style)
        self.add_pres_btn.grid(row=0, column=2, padx=5)
        self.print_record_btn = tk.Button(btn_frame, text="打印病历", command=self.print_record, **self.print_style)
        self.print_record_btn.grid(row=0, column=3, padx=5)
        self.print_pres_btn = tk.Button(btn_frame, text="打印处方", command=self.print_pres, **self.print_style)
        self.print_pres_btn.grid(row=0, column=4, padx=5)
        self.del_btn = tk.Button(btn_frame, text="删除病历", command=self.delete_record, **self.del_style)
        self.del_btn.grid(row=0, column=5, padx=5)
        tk.Button(btn_frame, text="返回", command=self._go_to_main, **self.back_style).grid(row=0, column=6, padx=5)