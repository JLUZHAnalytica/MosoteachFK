import json
import re
import os

from scrapy.selector import Selector


def load_html(filename):
    with open(filename, 'r') as fd:
        # 将网页转换Scrapy的Selector
        data = Selector(text=fd.read())
    return data


def parse_ans(ques):
    # 选择题目
    question = ques.css(".color-33.topic-subject").xpath("string()").get()
    if question not in ans_data:
        ans_data[question] = []
    # 在选项列表中循环
    for option in ques.css(".option-content"):
        # 检测是不是答案（通过颜色）
        if re.search(r"color:#07AC6C", option.attrib['style']):
            if option.css("img"):
                # 如果选项是公式或者图片
                ans_data[question].append(option.css("img").attrib['src'])
            else:
                # 正常选项提取，注意使用结尾的xpath方法
                ans_data[question].append(option.css(".person-result-answer").xpath("string()").get())

    return


ans_data = {}  # 用于存放结果的

for k in os.walk('key_html'):
    if k[0] != 'key_html':
        continue
    for filename in k[2]:
        if filename[-5:] != '.html':
            continue
        html = load_html(k[0] + '/' + filename)
        # 在题目列表中循环
        for ques in html.css(".row-center"):
            parse_ans(ques)

with open("data/question_data.json", 'w') as fd:
    fd.write(json.dumps(ans_data, ensure_ascii=False))
