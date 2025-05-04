# LMS练习和测验提取器

这个程序可以帮助您从岭南大学LMS系统中提取所有练习和测验题目，并将其保存为PDF文件。

## 环境要求

- Python 3.7+
- Chrome浏览器
- wkhtmltopdf（用于PDF转换）

## 安装步骤

1. 安装wkhtmltopdf：
   - Windows: 从 https://wkhtmltopdf.org/downloads.html 下载并安装
   - 确保将wkhtmltopdf添加到系统环境变量中

2. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 运行程序：
   ```bash
   python lms_scraper.py
   ```

2. 按提示输入您的LMS用户名和密码

3. 程序会自动：
   - 登录LMS系统
   - 提取所有练习和测验内容
   - 将内容保存为PDF文件（默认名称为：exercises_and_quizzes.pdf）

## 注意事项

1.setup这个脚本会：
自动安装所有必要的Python包（selenium, webdriver-manager, requests, pdfkit, beautifulsoup4）
检查wkhtmltopdf是否已正确安装
如果wkhtmltopdf未安装，会提供详细的安装指导
如果提示需要安装wkhtmltopdf：
访问 https://wkhtmltopdf.org/downloads.html
下载适合您Windows系统的安装包
运行安装程序
确保将安装目录添加到系统环境变量中

2.install_chrome_dirver这个脚本会：
尝试自动下载和安装正确版本的Chrome驱动
如果自动安装失败，会提供手动安装的指导
如果自动安装失败，请手动安装Chrome驱动：
打开Chrome浏览器
点击右上角三个点 -> 帮助 -> 关于Google Chrome，查看您的Chrome版本
访问 https://chromedriver.chromium.org/downloads
下载与您的Chrome版本匹配的驱动
将下载的chromedriver.exe放在程序目录下
安装完成后，运行主程序

- 请确保您有稳定的网络连接
- 程序运行过程中请不要关闭浏览器窗口
- 如果遇到登录问题，请确认您的用户名和密码是否正确
- 提取过程可能需要几分钟时间，请耐心等待
## 故障排除

如果遇到问题：

1. 确保已正确安装所有依赖
2. 检查Chrome浏览器是否已更新到最新版本
3. 确认wkhtmltopdf已正确安装并添加到环境变量
4. 如果遇到权限问题，请以管理员身份运行程序
