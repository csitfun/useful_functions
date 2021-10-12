import requests
import json
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import urllib

fakeHeaders = {'User-Agent': "Mozilla/4.0 (compatible; "
               "MSIE 6.0; Windows NT 5.1: SV1; "
               "AcooBrowser; .NET CLR 1.1.4322; "
               ".NET CLR 2.0.50727)"
               }
postData = {
    'username': '',
    'password': ''
}

# session = requests.session()
# login_url = 'https://sso.zxxk.com/login?service=https%3A%2F%2Fzujuan.xkw.com%2Fgzyy%2Fzsd29978%2F'
# response = session.post(login_url, data=postData, headers=fakeHeaders)
# print(response.status_code)
# print(response)

from selenium.webdriver.common.proxy import Proxy
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http:///183.159.84.172:18118')
# chrome_options = chrome_options
#login0 2o
browser = webdriver.Chrome(ChromeDriverManager().install())
login_url = 'https://sso.zxxk.com/login?service=https%3A%2F%2Fzujuan.xkw.com%2Fgzyy%2Fzsd29978%2F'
browser.get(login_url)
browser.find_element_by_class_name("lcon-weixin").click()
user = browser.find_element_by_id("username")
username = '13777895753'
password = 'zxcvbnm1'
user.send_keys(username)
browser.find_element_by_name("password").send_keys(password)
browser.find_element_by_id("CommonLogin").click()
time.sleep(10)
cookies_list = browser.get_cookies()
# print(cookies_list)
# url = "http
init_url = "https://zujuan.xkw.com/gzyy/zsd29981/qt2803o2p"

page_num = 1
count = 1
while True:
    url = init_url + str(page_num) + "/"
    print(url)
    browser.get(url)
    time.sleep(2)
    # html = session.get(url, data=postData, headers= fakeHeaders).text
    # print(html)
    # soup = BeautifulSoup(html, 'lxml')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    # question_text = soup.find_all('div', {'class': 'quesbox question'})
    questions = soup.find_all('div', {'class': "tk-test-item tk-quest-item quesroot "})
    page_num += 1
    for i in questions:
        try:
            detail_url = i.find('a', {'class': ' detail ctrl-btn'}).get('href')
            detail_url = "https://zujuan.xkw.com/" + detail_url
            browser.get(detail_url)
            detail_soup = BeautifulSoup(browser.page_source, 'lxml')
            Q_A = []
            for k in detail_soup.find('div', {'class': 'quest-cnt'}).stripped_strings:
                Q_A.append(k)
            knowledge = []
            for j in detail_soup.find('div', {'class': 'knowledges'}).stripped_strings:
                knowledge.append(j)
            question_id = detail_soup.find('div', {'class': 'questionid'})
            bank_id = detail_soup.find('div', {'class': 'bankid'})
            # answer_img_url = detail_soup.find().img['src']

            save_dict = {
                "count": "short_conv_" + str(count),
                "question_answer": Q_A,
                # "answer_img_url": answer_img_url,
                "knowledge": knowledge,
                "question_id": question_id,
                "bank_id": bank_id,
            }
            with open('result.json', 'a') as fp:
                json_str = json.dumps(save_dict)
                fp.write(json_str + "\n")
            print(save_dict)
            # urllib.request.urlretrieve(save_dict['answer_img_url'], 'D:\\short_conv_answer\\'+"short_conv_"+str(count)+".png")
            print("count:", count)
            count += 1
        except:
            continue
