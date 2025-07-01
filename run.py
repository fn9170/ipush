#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO Inspector - 启动脚本
这个脚本会检查环境配置，验证依赖包，并启动Flask应用
"""

import os
import sys
import subprocess
import importlib.util
import platform
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                     YOLO Inspector                          ║
    ║              AI驱动的目标检测与分析平台                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   请升级到Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_model_file():
    """检查模型文件"""
    print("🔍 检查模型文件...")
    model_path = Path("model/best.pt")
    
    if not model_path.exists():
        print("❌ 模型文件不存在: model/best.pt")
        print("   请确保模型文件位于正确路径")
        return False
    
    size_mb = model_path.stat().st_size / (1024 * 1024)
    print(f"✅ 模型文件存在: {size_mb:.1f}MB")
    return True

def check_required_packages():
    """检查必需的Python包"""
    print("🔍 检查依赖包...")
    
    required_packages = [
        ('flask', 'Flask'),
        ('ultralytics', 'ultralytics'),
        ('cv2', 'opencv-python'),
        ('PIL', 'Pillow'),
        ('numpy', 'numpy'),
        ('torch', 'torch')
    ]
    
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            if import_name == 'cv2':
                import cv2
            elif import_name == 'PIL':
                from PIL import Image
            else:
                importlib.import_module(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - 未安装")
            missing_packages.append(package_name)
    
    return missing_packages

def install_packages(packages):
    """安装缺失的包"""
    if not packages:
        return True
    
    print(f"\n📦 安装缺失的依赖包: {', '.join(packages)}")
    confirm = input("是否继续安装? (y/N): ").lower().strip()
    
    if confirm != 'y':
        return False
    
    try:
        # 尝试安装requirements.txt
        if Path("requirements.txt").exists():
            print("📦 使用requirements.txt安装依赖...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 依赖包安装成功")
                return True
            else:
                print(f"❌ 安装失败: {result.stderr}")
                return False
        else:
            print("❌ requirements.txt文件不存在")
            return False
            
    except Exception as e:
        print(f"❌ 安装过程出错: {str(e)}")
        return False

def create_directories():
    """创建必要的目录"""
    print("📁 创建必要的目录...")
    
    directories = ['uploads', 'results', 'templates']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}/")

def check_system_info():
    """显示系统信息"""
    print("💻 系统信息:")
    print(f"   操作系统: {platform.system()} {platform.release()}")
    print(f"   处理器: {platform.processor()}")
    print(f"   Python路径: {sys.executable}")
    
    # 检查GPU
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"   GPU支持: ✅ {gpu_count}个GPU - {gpu_name}")
        else:
            print(f"   GPU支持: ❌ 将使用CPU模式")
    except ImportError:
        print(f"   GPU支持: ❓ 无法检测（torch未安装）")

def get_local_ip():
    """获取本地IP地址"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def start_flask_app():
    """启动Flask应用"""
    print("\n🚀 启动Flask应用...")
    
    try:
        # 设置环境变量
        os.environ['FLASK_ENV'] = 'development'
        
        # 导入并运行app
        from app import app, load_model
        
        # 加载模型
        print("🤖 正在加载YOLOv8模型...")
        if not load_model():
            print("❌ 模型加载失败")
            return False
        
        print("✅ 模型加载成功")
        
        # 获取访问地址
        local_ip = get_local_ip()
        
        print("\n" + "="*60)
        print("🎉 应用启动成功!")
        print(f"📱 本地访问: http://localhost:5800")
        print(f"🌐 网络访问: http://{local_ip}:5800")
        print("🔄 按 Ctrl+C 停止服务")
        print("="*60 + "\n")
        
        # 启动Flask应用
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5800,
            use_reloader=False  # 避免重新加载模型
        )
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 启动错误: {str(e)}")
        return False

def main():
    """主函数"""
    print_banner()
    
    # 1. 检查Python版本
    if not check_python_version():
        input("\n按Enter键退出...")
        sys.exit(1)
    
    # 2. 显示系统信息
    check_system_info()
    print()
    
    # 3. 检查模型文件
    if not check_model_file():
        input("\n按Enter键退出...")
        sys.exit(1)
    
    # 4. 检查依赖包
    missing_packages = check_required_packages()
    
    if missing_packages:
        if not install_packages(missing_packages):
            print("\n❌ 依赖包安装失败，请手动安装:")
            print("   pip install -r requirements.txt")
            input("\n按Enter键退出...")
            sys.exit(1)
    
    # 5. 创建目录
    create_directories()
    
    # 6. 启动应用
    try:
        if not start_flask_app():
            input("\n按Enter键退出...")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止，感谢使用!")
    except Exception as e:
        print(f"\n❌ 意外错误: {str(e)}")
        input("\n按Enter键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main() 