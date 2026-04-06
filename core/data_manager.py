import json
import os
import sys
import time
from datetime import datetime, timedelta
import uuid


class DataManager:
    def __init__(self):
        # ========== 【打包EXE专用】路径修复 ==========
        # 获取程序真实运行路径（支持开发环境 + EXE环境）
        if hasattr(sys, '_MEIPASS'):
            # EXE 运行时
            self.base_dir = os.path.abspath(".")
        else:
            # 开发环境运行时
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # 数据文件夹统一放在 exe 同级目录的 data 文件夹
        self.data_dir = os.path.join(self.base_dir, "data")
        self.record_file = os.path.join(self.data_dir, "records.json")
        self.prescription_file = os.path.join(self.data_dir, "prescriptions.json")

        # 存储数据的列表
        self.records = []
        self.prescriptions = []
        # 自动创建数据文件夹
        os.makedirs(self.data_dir, exist_ok=True)
        # 启动时加载数据
        self.load_records()
        self.load_prescriptions()

    # 加载所有病历数据（增加数据格式校验）
    def load_records(self):
        try:
            if os.path.exists(self.record_file):
                with open(self.record_file, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
            else:
                self.records = []
            # 数据格式兜底
            self.records = [r for r in self.records if isinstance(r, dict) and "id" in r and "time" in r]
        except Exception as e:
            print(f"加载病历失败: {e}")
            self.records = []

    # 加载所有处方数据（增加数据格式校验）
    def load_prescriptions(self):
        try:
            if os.path.exists(self.prescription_file):
                with open(self.prescription_file, "r", encoding="utf-8") as f:
                    self.prescriptions = json.load(f)
            else:
                self.prescriptions = []
            # 数据格式兜底
            self.prescriptions = [p for p in self.prescriptions if isinstance(p, dict) and "record_id" in p]
        except Exception as e:
            print(f"加载处方失败: {e}")
            self.prescriptions = []

    # 保存病历数据（修复I/O报错）
    def save_records(self):
        try:
            with open(self.record_file, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存病历失败: {e}")

    # 保存处方数据（修复I/O报错）
    def save_prescriptions(self):
        try:
            with open(self.prescription_file, "w", encoding="utf-8") as f:
                json.dump(self.prescriptions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存处方失败: {e}")

    # 【核心修复】按类型获取最近2个月病历+倒序排序（解决空白bug）
    def get_records_by_type(self, type_name):
        # 过滤指定类型
        type_records = [r for r in self.records if r.get("type") == type_name]
        # 筛选最近2个月数据
        two_month_ago = datetime.now() - timedelta(days=60)
        recent_records = []
        for r in type_records:
            try:
                # 解析时间（兼容两种常见格式）
                record_time = datetime.strptime(r.get("time"), "%Y-%m-%d %H:%M:%S")
                if record_time >= two_month_ago:
                    recent_records.append(r)
            except:
                continue
        # 按就诊时间倒序排序（最新的在最前面）
        recent_records.sort(key=lambda x: x.get("time"), reverse=True)
        return recent_records

    # 根据病历ID获取关联的所有处方笺
    def get_prescriptions_by_record_id(self, record_id):
        pres = [p for p in self.prescriptions if p.get("record_id") == record_id]
        # 处方按创建时间倒序
        pres.sort(key=lambda x: x.get("time", ""), reverse=True)
        return pres

    # 新增病历
    def add_record(self, record):
        self.records.append(record)
        self.save_records()

    # 新增处方笺（自动生成唯一门诊号）
    def add_prescription(self, prescription):
        # 生成唯一门诊号（年月日+8位随机数）
        prescription["outpatient_no"] = datetime.now().strftime("%Y%m%d") + str(uuid.uuid4().int)[:8]
        prescription["id"] = str(uuid.uuid4())  # 处方唯一ID
        self.prescriptions.append(prescription)
        self.save_prescriptions()

    # 【新增】删除病历及关联的所有处方笺
    def delete_record_and_pres(self, record_id):
        # 删除病历
        self.records = [r for r in self.records if r.get("id") != record_id]
        # 删除关联处方
        self.prescriptions = [p for p in self.prescriptions if p.get("record_id") != record_id]
        # 保存数据
        self.save_records()
        self.save_prescriptions()
        return True

    # 【新增】更新病历数据
    def update_record(self, updated_record):
        for i, r in enumerate(self.records):
            if r.get("id") == updated_record.get("id"):
                self.records[i] = updated_record
                self.save_records()
                return True
        return False

    # 【新增】更新处方笺数据
    def update_prescription(self, updated_pres):
        for i, p in enumerate(self.prescriptions):
            if p.get("id") == updated_pres.get("id"):
                self.prescriptions[i] = updated_pres
                self.save_prescriptions()
                return True
        return False