import json
import time
import random
from pathlib import Path

# 数据文件路径
USER_DATA_PATH = "assets/users.json"
LOCK_DATA_PATH = "assets/lock.json"

class UserManager:
    def __init__(self):
        self.init_files()
        self.users = self.load_json(USER_DATA_PATH)
        self.lock_info = self.load_json(LOCK_DATA_PATH)

    def init_files(self):
        """初始化数据文件"""
        Path("assets").mkdir(exist_ok=True)
        for path in [USER_DATA_PATH, LOCK_DATA_PATH]:
            if not Path(path).exists():
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({}, f)

    def load_json(self, path):
        """加载JSON数据"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_json(self, data, path):
        """保存JSON数据"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # 登录锁定
    def check_lock(self, username):
        if username not in self.lock_info:
            return False
        lock_time = self.lock_info[username]["lock_time"]
        now = time.time()
        if now - lock_time < 86400:  # 24小时锁定
            return True
        # 超时自动解锁
        del self.lock_info[username]
        self.save_json(self.lock_info, LOCK_DATA_PATH)
        return False

    def get_lock_remaining(self, username):
        if username not in self.lock_info:
            return 0
        elapsed = time.time() - self.lock_info[username]["lock_time"]
        return max(0, 86400 - int(elapsed))

    def add_fail_count(self, username):
        if username not in self.lock_info:
            self.lock_info[username] = {"fail": 0, "lock_time": 0}
        self.lock_info[username]["fail"] += 1
        if self.lock_info[username]["fail"] >= 10:
            self.lock_info[username]["lock_time"] = time.time()
        self.save_json(self.lock_info, LOCK_DATA_PATH)

    # 注册
    def register(self, username, pwd, phone):
        if username in self.users:
            return False, "用户名已存在"
        self.users[username] = {
            "password": pwd,
            "phone": phone
        }
        self.save_json(self.users, USER_DATA_PATH)
        return True, "注册成功"

    # 登录验证
    def login(self, username, pwd):
        if self.check_lock(username):
            remain = self.get_lock_remaining(username)
            h = remain // 3600
            m = (remain % 3600) // 60
            return False, f"账号已锁定，剩余{h}小时{m}分钟解锁"
        if username not in self.users:
            self.add_fail_count(username)
            return False, "用户不存在，剩余登录次数：9"
        if self.users[username]["password"] == pwd:
            self.lock_info[username] = {"fail": 0, "lock_time": 0}
            self.save_json(self.lock_info, LOCK_DATA_PATH)
            return True, "登录成功！"
        else:
            self.add_fail_count(username)
            left = 10 - self.lock_info[username]["fail"]
            return False, f"密码错误，剩余{left}次登录机会"

    # 忘记密码-验证码
    def send_code(self, phone):
        """模拟发送验证码（可对接真实短信接口）"""
        code = random.randint(100000, 999999)
        self.sms_code = {phone: code}
        return code

    def reset_pwd(self, phone, code, new_pwd):
        if not hasattr(self, "sms_code") or self.sms_code.get(phone) != int(code):
            return False, "验证码错误"
        for name, info in self.users.items():
            if info.get("phone") == phone:
                self.users[name]["password"] = new_pwd
                self.save_json(self.users, USER_DATA_PATH)
                return True, "密码重置成功！"
        return False, "该手机号未注册"