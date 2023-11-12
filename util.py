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
    option.add_argument("--incognito")  # �޺�ģʽ
    option.add_argument("--disable-infobars")  # �����������ʾ���ܵ��Զ�����������Ŀ���
    option.add_experimental_option('excludeSwitches', ['enable-automation'])  # ʵ�ֹ�ܼ��
    option.add_experimental_option("detach", True)  # ��������Զ��ر�
    option.add_argument('--disable-gpu')  # ���ü���
    option.add_argument('window-size=1920x1080')  # ���÷ֱ�������վ�ķֱ���һ��
    option.add_argument('--start-maximized')  # ���ô������
    # ���õ���
    prefs = {
        'profile.default_content_setting_values': {
            'notifications': 2
        }
    }
    option.add_experimental_option('prefs', prefs)
    # ��ȡdriver����, �������úõ�option�����ȥ�����������������
    option.add_argument(
        'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')  # ���User-Agent�����������˰�
    option.add_experimental_option('useAutomationExtension', False)  # �����ݲ�����ΪFalse����һ��������һ���Ǳ�Ҫ��
    option.add_argument("--disable-blink-features=AutomationControlled")  # ���������֤
    web = webdriver.Chrome(options=option)
    return web


# def add_cookies(web,cookie_file):
#    with open(cookie_file,'r')as file:
#        cookie_list=json.load(file)
#       for cookie_dict in cookie_list:
#           if cookie_dict['secure']:#�������secure����������ȡ�������˴���if�ж��Ƿ���ڼ��Ƿ�Ϊtrue��
#               web.add_cookie(cookie_dict)

def add_cookies(web, cookie_file):
    with open(cookie_file, 'r') as file:
        cookie_list = json.load(file)
        for cookie_dict in cookie_list:
            #��Щcookie��domain��һ���޷�д����������
            try:
                web.add_cookie(cookie_dict)
            except:
                continue
