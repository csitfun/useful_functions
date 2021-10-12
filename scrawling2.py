import json
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

browser = webdriver.Chrome(ChromeDriverManager().install())
init_url = "https://www.koolearn.com/shiti/list-2-3-27705-"
page_num = 11519
count = 105126
while True:
    url = init_url + str(page_num) + ".html/"
    print(url)
    browser.get(url)
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    results = soup.find('div', {'class': 'i-page'}).find('div', {'class': 'i-content g-clear'})
    result1 = results.find('div', {'class': 'i-right p-right'})
    result2 = result1.find('div', {'class': 'p-results'})
    links = result2.find_all('div', {'class': 'i-timu'})
    page_num += 1
    for link in links:
        try:
            detail_url = link.find('a')['href']
            detail_url = "https://www.koolearn.com/" + detail_url
            browser.get(detail_url)
            detail_soup = BeautifulSoup(browser.page_source, 'lxml')
            detail = detail_soup.find('div', {'class': 'i-left'})
            Q_A = []
            detail1 = detail.find('div', {'class': 'i-panel p-panel'})
            for k in detail1.find('div', {'class': 'content'}).stripped_strings:
                Q_A.append(k)
            detail2 = detail.find('div', {'class': 'i-tab p-tab ji-tab p-single-tab'})
            answer = []
            for i in detail2.find('div', {'class': 'content'}).stripped_strings:
                answer.append(i)
            knowledge_soup = detail_soup.find('div', {'class': 'i-card'})
            knowledges = []
            for j in knowledge_soup.find('div', {'class': 'content'}).stripped_strings:
                knowledges.append(j)

            save_dict = {
                'count': str(count),
                'question': Q_A,
                'answer': answer,
                'knowledge': knowledges,
            }
            with open('tests.json', 'a') as fp:
                json_str = json.dumps(save_dict, ensure_ascii=False)
                fp.write(json_str + '\n')
            print(save_dict)
            print("count: ", count)
            count += 1
        except:
            continue
