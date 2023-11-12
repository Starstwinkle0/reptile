# @Time : 2023/11/4 13:29
# @Author: LZY
# @File: util.py
# @Software: PyCharm
import json
from selenium import webdriver


def create_chrome_driver(*, headless=False):
    option = webdriver.ChromeOptions()
    if headless:
        option.add_argument("--headless")
    option.add_argument("--incognito")  # 无痕模式
    option.add_argument("--disable-infobars")  # 禁用浏览器显示正受到自动化测试软件的控制
    option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 实现规避检测
    option.add_experimental_option("detach", True)  # 浏览器不自动关闭
    option.add_argument('--disable-gpu')  # 禁用加速
    option.add_argument('window-size=1920x1080')  # 设置分辨率与网站的分辨率一致
    option.add_argument('--start-maximized')  # 设置窗口最大化
    # 禁用弹窗
    prefs = {
        'profile.default_content_setting_values': {
            'notifications': 2
        }
    }
    option.add_experimental_option('prefs', prefs)
    # 获取driver对象, 并将配置好的option传入进去，并创建浏览器对象
    option.add_argument(
        'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')  # 添加User-Agent不用我描述了吧
    option.add_experimental_option('useAutomationExtension', False)  # 将传递参数改为False，这一步和下面一步是必要的
    option.add_argument("--disable-blink-features=AutomationControlled")  # 解决访问验证
    web = webdriver.Chrome(options=option)
    return web


# def add_cookies(web,cookie_file):
#    with open(cookie_file,'r')as file:
#        cookie_list=json.load(file)
#       for cookie_dict in cookie_list:
#           if cookie_dict['secure']:#如果存在secure属性则将其提取出来，此处的if判断是否存在即是否为true。
#               web.add_cookie(cookie_dict)

def add_cookies(web, cookie_file):
    with open(cookie_file, 'r') as file:
        cookie_list = json.load(file)
        for cookie_dict in cookie_list:
            #有些cookie，domain不一样无法写入跳过即可
            try:
                web.add_cookie(cookie_dict)
            except:
                continue
