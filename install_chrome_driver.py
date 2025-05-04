import os
import sys
import zipfile
import requests
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_version():
    """获取Chrome浏览器版本"""
    try:
        if sys.platform.startswith('win'):
            # Windows系统
            cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            version = output.strip().split()[-1]
        else:
            # Linux/Mac系统
            cmd = 'google-chrome --version'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            version = output.strip().split()[-1]
        return version.split('.')[0]  # 只返回主版本号
    except Exception as e:
        print(f"获取Chrome版本失败: {str(e)}")
        return None

def download_chrome_driver():
    print("开始安装Chrome驱动...")
    
    # 获取Chrome版本
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("无法获取Chrome版本，请确保Chrome浏览器已正确安装")
        return False
    
    print(f"检测到Chrome版本: {chrome_version}")
    
    try:
        # 下载对应版本的Chrome驱动
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{chrome_version}.0.0.0/win32/chromedriver-win32.zip"
        print(f"正在下载Chrome驱动...")
        
        # 下载文件
        response = requests.get(download_url, stream=True)
        if response.status_code != 200:
            print(f"下载失败，状态码: {response.status_code}")
            return False
            
        # 保存zip文件
        zip_path = "chromedriver.zip"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # 解压文件
        print("正在解压文件...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("chromedriver")
        
        # 移动chromedriver.exe到当前目录
        chromedriver_path = os.path.join("chromedriver", "chromedriver-win32", "chromedriver.exe")
        if os.path.exists(chromedriver_path):
            os.rename(chromedriver_path, "chromedriver.exe")
        
        # 清理临时文件
        os.remove(zip_path)
        import shutil
        shutil.rmtree("chromedriver")
        
        # 验证chromedriver是否可用
        print("验证Chrome驱动...")
        try:
            service = Service("chromedriver.exe")
            driver = webdriver.Chrome(service=service)
            driver.quit()
            print("Chrome驱动验证成功！")
        except Exception as e:
            print(f"Chrome驱动验证失败: {str(e)}")
            return False
        
        print("Chrome驱动安装成功！")
        return True
        
    except Exception as e:
        print(f"安装Chrome驱动失败: {str(e)}")
        return False

def main():
    print("=== Chrome驱动安装程序 ===")
    
    if download_chrome_driver():
        print("""
安装完成！

您现在可以运行主程序了：
python lms_scraper.py
""")
    else:
        print("""
安装失败！

请尝试以下步骤：
1. 确保您已安装最新版本的Chrome浏览器
2. 手动下载Chrome驱动：
   - 访问 https://googlechromelabs.github.io/chrome-for-testing/
   - 下载与您的Chrome浏览器版本匹配的驱动
   - 将chromedriver.exe放在程序目录下
""")

if __name__ == "__main__":
    main() 