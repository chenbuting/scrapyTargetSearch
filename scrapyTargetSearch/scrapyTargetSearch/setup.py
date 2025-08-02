from cx_Freeze import setup, Executable
import sys
import os

# 如果你在 Windows 系统上，确保添加 `Win32GUI` 来避免打开命令行窗口
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Scrapy 相关的模块和资源
includefiles = [
    # 包含 scrapy.cfg 和 Scrapy 项目文件夹
    "scrapy.cfg",  # Scrapy 项目的配置文件
    "myproject",  # 你的 Scrapy 项目文件夹
]

# 需要包括的模块（确保 Scrapy 及其依赖项都被包含）
packages = [
    "scrapy",
    "lxml",
    "scrapy.spiders", 
    "scrapy.crawler",
    # 其他 Scrapy 和爬虫依赖包
]

# 创建可执行文件
executables = [
    Executable("run_all.py", base=base)  # 入口脚本
]

# 打包配置
setup(
    name="BruceChen",
    version="0.1",
    description="BruceChen scrapyTargetSearch",
    options={
        "build_exe": {
            "packages": packages,  # 添加 Scrapy 和依赖
            "include_files": includefiles,  # 包括额外的文件和文件夹
        }
    },
    executables=executables  # 打包的可执行文件
)
