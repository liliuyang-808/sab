from selenium import webdriver
import re
import time
import numpy as np

dr = webdriver.Chrome()
dr.maximize_window()
dr.get('file:///D:/Code/JavaScript/un1/src/bank/index.html')

html = dr.page_source
timu = re.findall('<div class="sec_next">(.*?)</div>', html)  # 爬取答案

# 爬取题目 多做一步原因是要分出一题多少选项
xuxa_s = re.findall('<ul>(.*?)</ul>', html.replace("\n", ""))
xuxa = []
for i in xuxa_s:
    xuxa.append(re.findall('<label for=".*?">(.*?)</label>', i))
# 现在 xuxa列表里是[[A..,B..,C..,D..,E..],[A..],[A..,B..]]

button=[]#存储所有选线按钮
for nk in dr.find_elements_by_tag_name("input"):
    button.append(nk)
with open(r'./write.txt', encoding='utf-8') as f:
    res = f.read()
reo_timu=re.findall('题目:(.*?)\n',res)
reo_xuxa=re.findall('答案:(.*?)\n',res)

also=[]
also_txt=[]
number=[]
xuxa_index=[i for arr in xuxa for i in arr]#转成一维数组方便对齐索引
for i in range(0,len(timu)):
    if timu[i] in reo_timu:
        also_txt.append(reo_xuxa[reo_timu.index(timu[i])])#正确答案
    else:
        number.append(i)#备好选项后面
        also_txt.append(xuxa[i][0])#如果没有填入选项中第一项
for a in also_txt:
    lis = a.split('|')
    for j in lis:
        also.append(j)

#所有正确选项索引
index=[]
for i in also:
    index.append(xuxa_index.index(i))

#用正确答案索引点击按钮
for i in index:
    button[i].click()

input("提交后: ")

add_to = {}
lang=dr.page_source
temp = re.findall('<span>(.*?)</span>', lang)

for num in number:
    add_to[timu[num]]=temp[num]
print(add_to)

write_in = open(r'./write.txt', 'a', encoding='utf-8')  # 用可读写的权限打开txt
for code_a, answer_a in add_to.items():  # 同上一个for一样的道理
    write_in.write("题目:" + code_a + "\n")  # 存储正确的题目和正确答案
    write_in.write("答案:" + answer_a + "\n")  # 同上