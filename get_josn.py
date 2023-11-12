# @Time : 2023/4/29 23:40
# @Author: 龙智勇
# @File: get_json.py
# @Software: PyCharm
import json
from selenium import webdriver#导入需要进行测试的浏览器，我的是谷歌
from selenium.webdriver.common.by import By # 导入数据定位的系统
import time #用于每次点击事件后留给浏览器缓冲的时间。
from util import create_chrome_driver,add_cookies

web=create_chrome_driver(headless=False)

#进入登录页面
web.get('https://login.51job.com/login.php?lang=c&url=https%3A%2F%2Fwe.51job.com%2Fpc%2Fsearch')

# 填入登录
web.find_element(By.XPATH, '//*[@id="NormalLoginBtn"]/span[3]/a').click()
time.sleep(1)
web.find_element(By.ID, 'loginname').send_keys('15223217245')
time.sleep(2)
web.find_element(By.ID, 'password').send_keys('9951797934lZY$')
time.sleep(2)
web.find_element(By.XPATH, '//*[@id="isread_em"]').click()
time.sleep(2)
web.find_element(By.XPATH, '//*[@id="login_btn_withPwd"]').click()
time.sleep(15)  # 手动登录

#获取Cookie数据写入文件，
with open('./qcwy.json', 'w') as file:
    json.dump(web.get_cookies(),file)