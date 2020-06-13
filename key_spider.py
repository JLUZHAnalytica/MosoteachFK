# 这是一个还未完成的Spider

from selenium.webdriver import Chrome
from scrapy import Selector
import json
import time
import os


def login_by_userpass(web, username_value, password_value):
    uers = web.find_element_by_xpath('//*[@name="account_name"]')
    uers.send_keys(username_value)
    password = web.find_element_by_xpath('//*[@name="user_password"]')
    password.send_keys(password_value)
    login = web.find_element_by_xpath('//*[@id="login-button-1"]')
    login.click()
    time.sleep(3)


def login_by_cookies():
    with open("data/cookies.json") as fd:
        cookies = json.loads(fd.read())
    web = Chrome()
    web.get('https://www.mosoteach.cn/web/')
    for cookie in cookies:
        web.add_cookie(cookie)
    web.get('https://www.mosoteach.cn/web/')
    web.refresh()
    return web


def get_cookie_to_file():
    with open("access_file.txt", 'r') as fd:
        username_value = fd.readline()[:-1]
        password_value = fd.readline()
    web = Chrome()
    web.get('https://www.mosoteach.cn/web/')
    time.sleep(1)
    login_by_userpass(web, username_value, password_value)

    with open("data/cookies.json", 'w') as fd:
        fd.write(json.dumps(web.get_cookies(), indent=4))
    print("cookie保存成功")
    return web


def all_class_page_handle(web):
    page = Selector(text=web.page_source)
    index = 0
    for class_item in page.css(".my-join.class-list .class-item "):
        index += 1
        print(str(index) + ". " +class_item.css(".class-info-subject").attrib['text'])
    choose = input("请选择班课:")
    web.find_element_by_css_selector(".my-join.class-list .class-item:nth-of-type({})".format(choose)).click()



if __name__ == '__main__':
    if not os.path.exists("data/cookies.json"):
        web = get_cookie_to_file()
    else:
        web = login_by_cookies()
    all_class_page_handle(web)


