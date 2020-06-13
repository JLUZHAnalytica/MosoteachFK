# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author；鸿
from selenium.webdriver import Chrome
from lxml.etree import HTML
import time
from retrying import retry

def go_back():
    web.find_element_by_xpath('//*[@class="parents"]').click()


def write(string):
    with open('离散数学测试题.txt', 'a', encoding='utf-8')as f:
        f.write(string)

def write_html(title,string):
    with open('{}.html'.format(title), 'a', encoding='utf-8')as f:
        f.write(string)

def get_math(URL):
    web1 = Chrome(executable_path='E:\Google\Chrome\Application\chromedriver.exe')
    web1.get(URL)
    Maths = HTML(web1.page_source).xpath('//*[@font-family]')
    Math = ''.join([Math.xpath('string()') for Math in Maths])
    web1.close()
    return Math

@retry(stop_max_attempt_number=2, wait_random_min=1000, wait_random_max=2000)
def go_back(web):
    web.find_element_by_xpath('//*[@class="parents"]').click()

def get_QUIZ_data(web):
    html = HTML(web.page_source)
    title = html.xpath('//*[@id="interaction-title-box"]/div[1]/div[1]/@title')[0]
    write(title+'\n\n')
    write_html(title,web.page_source)
    #############问题
    questions = html.xpath('//*[@class="row-center"]')
    for i in range(1,len(questions)+1):
#         print(str(i),'ti')
        flag = 0
        question_s = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[1]/div/div[3]/pre/text()'.format(i))#[0].xpath('string()')
#         print(len(question_s))
        if len(question_s)>1 or len(question_s)==0:
            URL = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[1]/div/div[3]/pre/span/img/@src'.format(i))
            if URL == []:
                Math = ''
            else:
                Math = get_math(str(URL[0]))
            if len(question_s)!=0:
                question = str(Math).join(question_s)
            else:
                flag = 1
                question = str(Math)
        else:
            if flag==0:
                question = question_s[0]
        try:
            src = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[1]/div/div[3]/pre/img/@src'.format(i))[0]
            question = question +'\n'+ src
        except:
            pass
#     print(str(i)+'.'+question)
        write(str(i)+'.'+question+'\n')
#############选项
        opts = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[3]/div[.]'.format(i))
        for j in range(1,len(opts)+1):
            count = 0
            opt = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[3]/div[{}]'.format(i,j))[0].xpath('string()').replace('\n','').replace(' ','')
            try:
                opt_list = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[3]/div[{}]/span/span'.format(i,j))
                count = 1
                if len(opt_list)>1:
                    try:
                        URL = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[3]/div[{}]/span/span[{}]/img/@src'.format(i,j,len(opt_list)))[0]
                        opt_plus = get_math(str(URL))
                    except:
                        print(title+'第{}题{}号选项出现错误'.format(i,j))
                else:
                    URL = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[3]/div[{}]/span/span/img/@src'.format(i,j))[0]
                    opt_plus = get_math(str(URL))
            except:
                count = 0
            if count == 1:
                opt = opt + opt_plus
            try:
                src = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[3]/div[{}]/span[3]/img/@src'.format(i,j))[0]
                opt = opt + src
            except:
                pass
            write(opt+'\n')
#############正确答案
        answer = html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[2]/div[1]/div[1]'.format(i))[0].xpath('string()').replace('\n','').replace(' ','')
        write(answer+'\n\n')
    print(title,'页面爬取成功...')



# except:
#     pass
def main1(web,uersname,password):
    uers = web.find_element_by_xpath('//*[@name="account_name"]')
    uers.send_keys('{}'.format(uersname))
    time.sleep(1)
    pd = web.find_element_by_xpath('//*[@name="user_password"]')
    pd.send_keys('{}'.format(password))
    time.sleep(1)
    login = web.find_element_by_xpath('//*[@id="login-button-1"]')
    login.click()
    time.sleep(1)
    Discretemathematics = web.find_element_by_xpath('//*[@title="离散数学"]')
    Discretemathematics.click()
    # try:
    r = str(input('是否助教(y|n):'))
    if r=='y':
        button = web.find_element_by_xpath('//*[@class="button-routine button-sure select-role-student"]')
        time.sleep(1)
        button.click()
    bu = web.find_elements_by_xpath('//*[@class="group-name color-33"]')
    for b in range(1,len(bu)):
        time.sleep(1)
        bu[b].click()
    QUIZ = web.find_elements_by_xpath('//*[@data-type="QUIZ"]')
    for a in range(0,len(QUIZ)):
        QUIZ[a].click()
        time.sleep(1)
        html = HTML(web.page_source)
        try:
            begin_test = html.xpath('//*[@class="button-routine"]')[0].xpath('string()')
        except:
            begin_test = ''
        if begin_test =='开始测试':
            time.sleep(1)
            go_back(web)
        else:
            get_QUIZ_data(web)
            go_back(web)
        QUIZ = web.find_elements_by_xpath('//*[@data-type="QUIZ"]')


def main2(web,uersname,password):
    uers = web.find_element_by_xpath('//*[@name="account_name"]')
    uers.send_keys('{}'.format(uersname))
    time.sleep(1)
    passwords = web.find_element_by_xpath('//*[@name="user_password"]')
    passwords.send_keys('{}'.format(password))
    time.sleep(1)
    login = web.find_element_by_xpath('//*[@id="login-button-1"]')
    login.click()
    time.sleep(1)
    datastruct = web.find_element_by_xpath('//*[@id="main"]/main/section[2]/div[3]/ul/li[1]/div[1]/img')
    datastruct.click()
    time.sleep(1)
    html = web.page_source
    html = HTML(html)
    test = html.xpath('//*[@data-type="QUIZ"]/@data-url')
    f = open('数据结构测试题.txt', 'a', encoding='utf-8')
    for count in range(len(test)):
        url = test[count]
        if 'https://' in url:
            web.get(url)
            Key = web.find_element_by_xpath('//*[@id="member-list-box"]/div[1]/div[2]/a[1]')
            Key.click()
            question_html = web.page_source
            question_html = HTML(question_html)
            titles = question_html.xpath('//*[@id="interaction-title-box"]/div[1]/div[1]')[0].xpath('string()')
            ###问题选项以及正确答案
            # print(title,'\n')
            write_html(titles,web.page_source)
            title = titles + '\n\n'
            f.write(title)
            ques_list = question_html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[.]/div[1]/div/div[1]/div/div[3]/pre')
            i = 1
            for ques_s in ques_list:
                ques = ques_s.xpath('string()')
                opt = question_html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[3]/div[.]'.format(i))
                question = str(i) + '.' + ques_list[i - 1].xpath('string()') + '\n'
                # print(question)
                f.write(question)
                for j in range(1, len(opt) + 1):
                    opt = question_html.xpath(
                        '//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[1]/div/div[3]/div[{}]/span[3]'.format(i, j))[0]
                    opt = opt.xpath('string()').replace('\n', '')
                    # print(opt)
                    opt = opt + '\n'
                    f.write(opt)
                answer = question_html.xpath('//*[@id="cc-main"]/div[2]/div[4]/div[{}]/div[2]/div[1]/div[1]'.format(i))[
                    0].xpath('string()')
                answer = answer.replace(' ', '').replace('\n', '')
                # print(answer,'\n')
                answer = answer + '\n\n'
                f.write(answer)
                i += 1
        print(titles+'页面爬取成功...')
    f.close()

if __name__ == '__main__':
    print('1:数据结构')
    print('2.离散数学')
    result = str(input('请选择需要爬取的课程：'))
    username = str(input("username:"))
    password = str(input("password:"))
    web = Chrome()#executable_path='E:\Google\Chrome\Application\chromedriver.exe'路径自己添加下
    time.sleep(1)
    web.get('https://www.mosoteach.cn/web/')
    time.sleep(1)
    if result=='1':
        main2(web,username,password)
    elif result=='2':
        main1(web,username,password)
    web.close()