from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pdfkit
import os
import traceback
import sys

class LMSScraper:
    def __init__(self):
        print("初始化LMSScraper...")
        self.url = "https://lms.ln.edu.hk/course/view.php?id=46716"
        self.setup_driver()
        
    def setup_driver(self):
        print("设置Chrome驱动...")
        try:
            chrome_options = Options()
            # chrome_options.add_argument('--headless')  # 无头模式，取消注释以启用
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--disable-extensions')
            
            print("正在下载Chrome驱动...")
            try:
                # 尝试使用webdriver_manager安装驱动
                driver_path = ChromeDriverManager().install()
                print(f"Chrome驱动下载路径: {driver_path}")
                service = Service(driver_path)
            except Exception as e:
                print(f"使用webdriver_manager安装驱动失败: {str(e)}")
                print("尝试使用本地Chrome驱动...")
                # 如果webdriver_manager失败，尝试使用本地Chrome驱动
                if sys.platform.startswith('win'):
                    driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
                else:
                    driver_path = os.path.join(os.getcwd(), 'chromedriver')
                service = Service(driver_path)
            
            print("正在启动Chrome浏览器...")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Chrome浏览器启动成功！")
        except Exception as e:
            print(f"设置Chrome驱动失败: {str(e)}")
            print("详细错误信息:")
            print(traceback.format_exc())
            raise
        
    def login(self, username, password):
        try:
            print(f"正在访问 {self.url}...")
            self.driver.get(self.url)
            
            print("等待登录表单加载...")
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_field = self.driver.find_element(By.ID, "password")
            
            print("输入登录信息...")
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            print("点击登录按钮...")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            login_button.click()
            
            print("等待页面加载...")
            time.sleep(5)
            
            # 检查是否登录成功
            if "login" in self.driver.current_url.lower():
                print("登录失败：用户名或密码错误")
                return False
                
            print("登录成功！")
            return True
            
        except Exception as e:
            print(f"登录过程出错: {str(e)}")
            print("详细错误信息:")
            print(traceback.format_exc())
            return False
            
    def extract_exercises_and_quizzes(self):
        try:
            print("等待课程内容加载...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "course-content"))
            )
            
            print("搜索练习和测验...")
            exercises = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Exercise') or contains(text(), 'Quiz')]")
            print(f"找到 {len(exercises)} 个练习和测验")
            
            content = []
            for i, exercise in enumerate(exercises, 1):
                try:
                    title = exercise.text
                    print(f"正在处理第 {i} 个: {title}")
                    content.append(f"<h2>{title}</h2>")
                    
                    print("点击进入练习页面...")
                    exercise.click()
                    time.sleep(2)
                    
                    print("获取练习内容...")
                    exercise_content = self.driver.find_element(By.CLASS_NAME, "content").get_attribute('innerHTML')
                    content.append(exercise_content)
                    
                    print("返回课程页面...")
                    self.driver.back()
                    time.sleep(2)
                except Exception as e:
                    print(f"处理练习 {title} 时出错: {str(e)}")
                    continue
            
            return "\n".join(content)
            
        except Exception as e:
            print(f"提取内容失败: {str(e)}")
            print("详细错误信息:")
            print(traceback.format_exc())
            return None
            
    def save_to_pdf(self, content, output_file="exercises_and_quizzes.pdf"):
        try:
            print("创建临时HTML文件...")
            with open("temp.html", "w", encoding="utf-8") as f:
                f.write(f"""
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        h2 {{ color: #333; }}
                    </style>
                </head>
                <body>
                    {content}
                </body>
                </html>
                """)
            
            print("转换为PDF...")
            pdfkit.from_file("temp.html", output_file)
            
            print("清理临时文件...")
            os.remove("temp.html")
            print(f"PDF已保存为: {output_file}")
            
        except Exception as e:
            print(f"保存PDF失败: {str(e)}")
            print("详细错误信息:")
            print(traceback.format_exc())
            
    def close(self):
        print("关闭浏览器...")
        self.driver.quit()

def main():
    try:
        print("=== LMS练习和测验提取器 ===")
        scraper = LMSScraper()
        
        # 请替换为您的登录信息
        username = input("请输入您的用户名: ")
        password = input("请输入您的密码: ")
        
        if scraper.login(username, password):
            content = scraper.extract_exercises_and_quizzes()
            if content:
                scraper.save_to_pdf(content)
        
        scraper.close()
        
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        print("详细错误信息:")
        print(traceback.format_exc())
    finally:
        print("程序结束")

if __name__ == "__main__":
    main() 