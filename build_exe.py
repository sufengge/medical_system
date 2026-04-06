import PyInstaller.__main__
import os
import sys

# 项目路径（自动获取）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 打包命令（单文件、无窗口、离线独立运行）
PyInstaller.__main__.run([
    os.path.join(BASE_DIR, "main.py"),
    "--onefile",          # 打包成单个exe
    "--windowed",         # 不显示黑色控制台
    "--noconsole",
    "--name=医疗病历管理系统",  # exe文件名
    "--icon=icon.ico",        # 无图标（你有图标可以替换）
    "--clean",
    "--noconfirm",
])