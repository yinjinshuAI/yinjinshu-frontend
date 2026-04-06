#!/usr/bin/env python3
"""
生成 CloudBase 第 14 版部署包
修复点：
1. Dockerfile 不再依赖外部 logs 目录，改为在容器内自动创建
2. 移除 logs 目录相关的 COPY 指令
预计构建时间：3-5 分钟
"""

import os
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path(r"C:\Users\Mac\.real\users\user-aa8a8dbf1bb1240c579394d41011f8d6\workspace")
PROJECT_DIR = WORKSPACE / "yinjinshu-ai-assistant"
DEPLOY_ZIP = WORKSPACE / "yinjinshu-ai-assistant-deploy-v14.zip"
TEMP_DIR = WORKSPACE / "deploy-build-temp-v14"

def main():
    print("=" * 60)
    print("🚀 开始生成第 14 版部署包（彻底解决 logs 问题）")
    print("=" * 60)
    
    # 清理旧文件
    if DEPLOY_ZIP.exists():
        DEPLOY_ZIP.unlink()
        print("✅ 已删除旧的部署包")
    
    # 创建临时目录
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    print("✅ 已创建临时构建目录")
    
    # 复制项目文件（排除 logs 目录，因为 Dockerfile 已改为在容器内创建）
    for item in PROJECT_DIR.iterdir():
        if item.name in ['.git', 'deploy-build-temp', '__pycache__', '.pytest_cache', 'logs']:
            continue  # 跳过 Git、缓存、临时目录和 logs（不需要了）
        if item.is_dir():
            shutil.copytree(item, TEMP_DIR / item.name)
        else:
            shutil.copy2(item, TEMP_DIR / item.name)
    print("✅ 已复制项目文件（已排除 logs 目录）")
    
    # 压缩为 ZIP
    print("⏳ 正在压缩 ZIP 包...")
    with zipfile.ZipFile(DEPLOY_ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(TEMP_DIR)
                zipf.write(file_path, arcname)
    print("✅ 已生成 ZIP 压缩包")
    
    # 清理临时目录
    shutil.rmtree(TEMP_DIR)
    print("✅ 已清理临时目录")
    
    # 显示结果
    zip_size = DEPLOY_ZIP.stat().st_size / 1024
    print("\n" + "=" * 60)
    print("✅ 第 14 版部署包生成成功！")
    print("=" * 60)
    print(f"📦 文件名：{DEPLOY_ZIP.name}")
    print(f"📏 大小：{zip_size:.2f} KB")
    print(f"📍 路径：{DEPLOY_ZIP.absolute()}")
    print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\n🎯 关键修复：")
    print("   • Dockerfile 改为在容器内创建 logs 目录")
    print("   • 不再依赖外部 logs 目录（已排除在 ZIP 包外）")
    print("   • 预计构建时间：3-5 分钟")
    print("\n📋 下一步操作：")
    print("   1. 打开腾讯云 CloudBase 控制台")
    print("   2. 进入云托管 -> yinjinshuservice -> 版本管理")
    print("   3. 上传此 ZIP 文件（确认大小约 {:.2f} KB）".format(zip_size))
    print("   4. 等待构建完成（3-5 分钟）")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("\n💡 提示：请检查项目目录路径是否正确")
        import traceback
        traceback.print_exc()
        exit(1)