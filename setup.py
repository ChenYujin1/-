import subprocess
import sys
import os

def install_requirements():
    print("开始安装必要的Python包...")
    
    # 读取requirements.txt中的依赖
    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()
    
    # 安装每个依赖
    for requirement in requirements:
        print(f"正在安装 {requirement}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"成功安装 {requirement}")
        except subprocess.CalledProcessError as e:
            print(f"安装 {requirement} 失败: {str(e)}")
            return False
    
    print("\n所有Python包安装完成！")
    return True

def check_wkhtmltopdf():
    print("\n检查wkhtmltopdf安装...")
    try:
        # 尝试运行wkhtmltopdf --version
        subprocess.check_call(['wkhtmltopdf', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("wkhtmltopdf已正确安装！")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("""
wkhtmltopdf未安装或未添加到系统环境变量中。
请按照以下步骤安装wkhtmltopdf：

1. 访问 https://wkhtmltopdf.org/downloads.html
2. 下载适合您系统的安装包
3. 运行安装程序
4. 确保将安装目录添加到系统环境变量中

安装完成后，请重新运行此脚本。
""")
        return False

def main():
    print("=== LMS练习和测验提取器安装程序 ===")
    
    # 安装Python包
    if not install_requirements():
        print("Python包安装失败，请检查错误信息。")
        return
    
    # 检查wkhtmltopdf
    if not check_wkhtmltopdf():
        return
    
    print("""
安装完成！

您现在可以运行程序了：
python lms_scraper.py
""")

if __name__ == "__main__":
    main() 