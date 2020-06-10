import json
import os
import random
import time

from scrapy.selector import Selector
import Levenshtein  # pip install python-Levenshtein
from lxml.etree import HTML
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def right_scope(web, ques_index, opt_index):
    # 利用js将元素拖动到可见区域
    WebDriverWait(web, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, opt_index + 2))))
    element = web.find_element_by_xpath('//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, opt_index + 2))
    web.execute_script('arguments[0].scrollIntoView({block:"center"});', element)  # 可见元素与页面“中间”对齐


def verify_ans(ques, ans, database):
    for a in database[ques]:
        if a == ans:
            return True
    return False


web = Chrome()
web.get(
    "file:///Users/yokey/OneDrive/Develop/%E4%BA%91%E7%8F%AD%E8%AF%BE/quiz_html/%E4%BA%91%E7%8F%AD%E8%AF%BE%20-%20%E5%BC%80%E5%A7%8B%E7%AD%94%E9%A2%98_bug.html")

with open("question_data.json", 'r') as fd:
    quiz_database = json.loads(fd.read())
quiz_page = Selector(text=web.page_source)
ques_index = 0
for quiz in quiz_page.css(".student-topic-row"):
    opt_index = 0
    question = ''
    if ques_index == 4:
        print()
    for sel_opt in quiz.css("pre"):
        sel_text = sel_opt.xpath("string()").get()
        if opt_index == 0:
            question = sel_text
            opt_index += 1
            continue
        if sel_opt.css("img"):
            if verify_ans(question, sel_opt.css("img").attrib['src'], quiz_database):
                right_scope(web, ques_index, opt_index)
                web.find_element_by_xpath('//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, opt_index + 2)).click()
        else:
            if verify_ans(question, sel_text, quiz_database):
                right_scope(web, ques_index, opt_index)
                web.find_element_by_xpath('//*[@id="topics-box"]/div[{}]/div[{}]'.format(ques_index + 1, opt_index + 2)).click()
        opt_index += 1
    ques_index += 1
