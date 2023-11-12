# @Time : 2023/10/4 12:33
# @Author: LZY
# @File: qcwy_class.py
# @Software: PyCharm

from selenium import webdriver  # 导入需要进行测试的浏览器，我的是谷歌
from selenium.webdriver.common.by import By  # 导入数据定位的系统
from selenium.webdriver.common.keys import Keys  # 用于把键盘上的按钮的命令输入
# 导入动作链对应的类
from selenium.webdriver import ActionChains
# 反检测
from selenium.webdriver import ChromeOptions
from time import sleep
import time  # 用于每次点击事件后留给浏览器缓冲的时间。
from random import randint  # 随机时间
import csv
from util import add_cookies,create_chrome_driver


# 写入一个类，方便以后方法的调用
class DRenSpider:  # 不要写小括号，不然就是方法
    # 各个方法的返回变量，init方法里定义的所有变量在同一个类中能够通用,类似与全局变量
    def __init__(self):
        self.loginweb = r'https://login.51job.com/login.php?lang=c&url=https%3A%2F%2Fwe.51job.com%2Fpc%2Fsearch'  # 设置登录的网站
        self.baseweb = r'https://we.51job.com/pc/search?jobArea=080200&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88&searchType=2&sortType=0&metro='  # 设置最初的爬取网址
        self.web = create_chrome_driver(headless=False)  # 设置爬取的对象
        f = open(r'D:\Skills\python\reptile\Dynamic_web_crawling\selenium\ Project_1_Recruitment\job\hangzhou\data\qcwy_杭州.csv', mode='a', encoding='utf-8', newline='')  # mode='a',表示接着写，不覆盖。，mode=‘w’,则表示从第一行开始写
        self.csvwirter = csv.writer(f)  # 设置csv写字对象

    # 设置浏览器
    # def set_web(self):
    #     # 无头浏览器
    #     option = webdriver.ChromeOptions()
    #     option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 实现规避检测
    #     option.add_experimental_option("detach", True)  # 浏览器不自动关闭
    #     # option.add_argument('--headless')
    #     option.add_argument('--disable-gpu')
    #     option.add_argument("--window-size=1920,1080")  # 设置分辨率与网站的分辨率一致
    #     option.add_argument('--start-maximized')  # 设置窗口最大化
    #     # 获取driver对象, 并将配置好的option传入进去，并创建浏览器对象
    #     option.add_argument(
    #         'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')  # 添加User-Agent不用我描述了吧
    #     option.add_experimental_option('useAutomationExtension', False)  # 将传递参数改为False，这一步和下面一步是必要的
    #     option.add_argument("--disable-blink-features=AutomationControlled")  # 解决访问验证
    #     web = webdriver.Chrome(options=option)
    #     return web

    # 连接最开始的爬取网站
    def get_link(self):
        self.web.get(self.loginweb)
        add_cookies(self.web, 'qcwy.json')  # 把cookie形成josn文件进行导入
        self.web.get(self.baseweb)

    # 获取数据
    def get_data(self):
        div_list = self.web.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div')
        # print(div_list)#验证是否获取到div了
        for div in div_list:
            data = []
            job_name = div.find_element(By.XPATH, './div[2]/div[1]/div/span').text
            # print(job_name)
            try:
                job_address = div.find_element(By.XPATH, './div[2]/div[1]/p/span[2]/span[1]').text.split('·')[1]
            except:
                job_address = ''
            # print(job_address)

            try:
                all_money = div.find_element(By.XPATH, './div[2]/div[1]/p/span[1]').text
                x = all_money.split("-")[0]
                y = all_money.split('-')[1].split('·')[0].split('/')[0]
                z = y[-1]
                if '千' in x:
                    x = ''.join(x.split('千'))
                    job_money = float(x) * 1000
                elif '万' in x:
                    x = ''.join(x.split('万'))
                    job_money = float(x) * 10000
                elif z == '千':
                    job_money = float(x) * 1000
                elif z == '万':
                    job_money = float(x) * 10000
                elif z == '年':
                    job_money = float(x) / 12 * 10000
            except:
                job_money = ''
            # print(job_money)

            job_company = div.find_element(By.XPATH, './div[2]/div[2]/div[2]/a').text
            # print(job_company)
            try:
                company_type = div.find_element(By.XPATH, './div[2]/div[2]/div[2]/p/span[2]').text.split('|')[0].strip()
            except:
                company_type = '通用'
            # print(company_type)
            try:
                education = div.find_element(By.XPATH, './div[2]/div[1]/p/span[2]/span[3]').text
            except:
                education = '无要求'
            # print(education)
            try:
                company_introduce = div.find_element(By.XPATH,'div[2]/div[2]/div[2]/p/span[1]').text  # //*[@id="app"]/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/p[1]
            except:
                education = '无要求'
            # print(company_introduce)
            data.extend([job_company, company_type, job_name, job_address, job_money, education, company_introduce])
            self.csvwirter.writerow(data)

    # 设置循环爬取
    def set_circulate(self):
        # self.web.maximize_window()  # 界面最大化
        i = 1
        for page in range(0, 50):
            time.sleep(randint(3, 6))
            # 滚动到浏览器底部,防止有些数据要滚动才会刷新同时模拟人的行为（不）同时加载动态数据
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            self.web.execute_script(js)
            # break
            self.get_data()
            # 点击下一页
            try:
                self.web.find_element(By.CLASS_NAME, 'btn-next').click()  # 点击下一页
            except:
                continue
            finally:
                print('记录好%d页' % i)
                i = i + 1

    # 函数运行顺序，一般来说在所有的方法都写完之后再次编排
    def spider(self):
        title = ('job_company', 'company_type', 'job_name', 'job_address', 'job_money', 'education', 'company_introduce')
        self.csvwirter.writerow(title)  # 写入标题
        self.get_link()  # 进入基础网站
        self.set_circulate()  # 设置循环


# 运行此类中的函数
DRenSpider().spider()
