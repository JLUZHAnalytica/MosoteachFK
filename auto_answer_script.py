# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author；鸿, Yokey

import json
import os
import time

from scrapy.selector import Selector
from lxml.etree import HTML
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# def get_equal_rate(str1, str2):
#     return Levenshtein.ratio(str1, str2)


def init_web():
    web = Chrome()
    time.sleep(1)
    web.get('https://www.mosoteach.cn/web/')
    time.sleep(1)
    uers = web.find_element_by_xpath('//*[@name="account_name"]')
    uers.send_keys(username_value)
    password = web.find_element_by_xpath('//*[@name="user_password"]')
    password.send_keys(password_value)
    login = web.find_element_by_xpath('//*[@id="login-button-1"]')
    login.click()
    time.sleep(1)
    Discretemathematics = web.find_element_by_xpath('//*[@title="离散数学"]')
    Discretemathematics.click()
    time.sleep(1)
    r = str(input('是否助教(y|n):'))
    if r == 'y':
        button = web.find_element_by_xpath('//*[@class="button-routine button-sure select-role-student"]')
        time.sleep(1)
        button.click()
    time.sleep(1)
    QUIZ = web.find_elements_by_xpath('//*[@data-type="QUIZ"]')
    bu = web.find_elements_by_xpath('//*[@class="group-name color-33"]')
    for b in range(1, len(bu)):
        bu[b].click()
        time.sleep(0.5)  # 太低会导致展开不完全

    return web


def get_unaccomplished(web):
    """返回web的xpath对象 和 标题"""
    titles_xpath_1 = HTML(web.page_source).xpath('//*[@style="color:#EC6941;"]')
    titles = HTML(web.page_source).xpath('//*[@data-type="QUIZ"]/div/div[1]/span[2]/@title')
    titles_color_xpath = HTML(web.page_source).xpath('//*[@data-type="QUIZ"]/div/div[3]/div/span[11]/@style')
    titles_web = web.find_elements_by_xpath('//*[@style="color:#EC6941;"]')
    titles_list = []
    title_web_list = []
    titles_xpath = []
    for j in range(len(titles_xpath_1)):
        if titles_xpath_1[j].xpath('string()') == '5 经验':
            title_web_list.append(titles_web[j])
            titles_xpath.append(titles_xpath_1[j])
    title_web_list = title_web_list[:-1]
    titles_xpath = titles_xpath[:-1]
    for j in range(len(titles_color_xpath)):
        if titles_color_xpath[j] == 'color:#EC6941;':
            titles_list.append(titles[j])
    return title_web_list, titles_list


def verify_ans(ques, ans, database):
    for a in database[ques]:
        if a == ans:
            return True
    return False


def right_scope(web, ques_index, opt_index):
    # 利用js将元素拖动到可见区域
    WebDriverWait(web, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, opt_index + 2))))
    element = web.find_element_by_xpath('//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, opt_index + 2))
    web.execute_script('arguments[0].scrollIntoView({block:"center"});', element)  # 可见元素与页面“中间”对齐


def finish_quiz(web, no_left_mode):
    with open("data/question_data.json", 'r', encoding='utf-8') as fd:
        quiz_database = json.loads(fd.read())
    quiz_page = Selector(text=web.page_source)
    ques_index = 0
    for quiz in quiz_page.css(".student-topic-row"):
        opt_index = 0
        question_title = ''
        cur_question_done = False
        for sel_opt in quiz.css("pre"):
            sel_text = sel_opt.xpath("string()").get()
            if opt_index == 0:
                question_title = sel_text
                opt_index += 1
                continue
            if sel_opt.css("img"):
                if verify_ans(question_title, sel_opt.css("img").attrib['src'], quiz_database):
                    right_scope(web, ques_index, opt_index)
                    web.find_element_by_xpath(
                        '//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, opt_index + 2)).click()
                    cur_question_done = True
            else:
                if verify_ans(question_title, sel_text, quiz_database):
                    right_scope(web, ques_index, opt_index)
                    web.find_element_by_xpath(
                        '//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, opt_index + 2)).click()
                    cur_question_done = True
            opt_index += 1
        '''查询不到答案随机选，默认关闭'''
        if no_left_mode and not cur_question_done:
            print("第{}题：{}已自动选择。".format(ques_index + 1, question_title))
            web.find_element_by_xpath('//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, 4)).click()
        ques_index += 1


def go_back(web):
    web.find_element_by_xpath('//*[@class="parents"]').click()


def main(web, no_left_mode):
    title_web_list, titles_list = get_unaccomplished(web)
    print('当前未完成的测试如下：')
    for count in range(len(titles_list)):
        print(str(count + 1) + '.' + titles_list[count])
    ID = int(input('\n请选择需要答题的序号(输入-1退出程序):'))
    if ID == -1:
        return False
    title_web_list[ID - 1].click()  # 进入答题页面
    time.sleep(1)
    begin_test = web.find_element_by_xpath('//*[@class="button-routine"]')
    begin_test.click()  # 开始答题
    js = "var q=document.documentElement.scrollTop={}".format(350)
    web.execute_script(js)
    finish_quiz(web, no_left_mode)
    if input("本次是否自动提交: (y/n)") == 'n':
        input("请手动提交后按回车继续...")
    else:
        web.find_element_by_xpath('//*[@class="button-routine submit-button"]').click()
        web.find_element_by_xpath('//*[@class="button-routine tips-ok"]').click()
        time.sleep(1)
    try:  # 处理随机弹出的提示框
        web.find_element_by_xpath('//*[@class="button-routine tips-ok"]').click()
    except:
        pass
    time.sleep(1)
    score = HTML(web.page_source).xpath('//*[@id="score-bg"]/div[2]/span[1]')[0].xpath('string()').replace('\n', '').replace(' ', '')
    Time = HTML(web.page_source).xpath('//*[@id="time-bg"]/div[2]/span')[0].xpath('string()').replace('\n', '').replace(' ', '')
    time.sleep(1)
    print('您的得分为：' + str(score) + '分，用时：' + Time)
    # web.find_element_by_xpath('//*[@class="button-routine tips-ok"]').click()
    # time.sleep(2)
    '''答完题返回'''
    go_back(web)
    return True


username_value = ''
password_value = ''


def run():
    web = init_web()
    if str(input('是否随机选模式(如果开启题目匹配不到答案)(y|n):')) == 'y':
        no_left_mode = True
    else:
        no_left_mode = False
    continue_quiz = True
    while continue_quiz:
        continue_quiz = main(web, no_left_mode)
        # os.system("cls")


if __name__ == '__main__':
    with open("access_file.txt", 'r') as fd:
        username_value = fd.readline()[:-1]
        password_value = fd.readline()
    run()
