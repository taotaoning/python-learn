import requests
import random
import re
from bs4 import BeautifulSoup
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 设置无头浏览器
chrome_options = Options()
# chrome_options.add_argument('--headless')


print(os.getcwd())

# 免费代理ip地址
proxy_url='http://www.xiladaili.com/gaoni/{0}/'




# 读取头信息文件
def getUserAget():
    list_agents=[]
    with open('bilibili-spider\\user_agents.txt','r') as agents:
        for ua in agents.readlines():
            list_agents.append(ua.strip())
        return list_agents

# 请求代理网址，目前爬取20页进行挑选
def doRequest(pages):
    list_proxy_ips=[]
    ua=random.choice(getUserAget())
    # 请求头
    headers={
        'User-Agent':ua,
        'Referer':'http://www.xiladaili.com/'
    }

    for item in range(1,pages):
        # 中间暂停2秒钟，避免请求频率过高
        time.sleep(2)
        doReuestProxy(item,list_proxy_ips,headers)

    return list_proxy_ips
    # result=re.findall('(2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2}',res.text)
    # tags=soup.find_all('tr')
    # for tag in tags.children:
    #     print(tag)
    # print(result)

def doReuestProxy(page,ips,headers):

    request_url=proxy_url.format(str(page))

    res=requests.session().get(request_url,headers=headers)

  
    soup=BeautifulSoup(res.content,'html.parser')

    trs=soup.table.tbody.find_all('tr')
    for tr in trs:
        ips.append(tr.contents[1].string)
    
# 构建代理请求，请求b站,过滤不可用ip
def filterAvailableIps(ips,ava_ips):

    uas=getUserAget()

    for ip in ips:
        ua=random.choice(uas)

        # 请求头
        headers={
            'User-Agent':ua,
            'origin':'https://space.bilibili.com',
            'Referer':'https://space.bilibili.com'
        }

        proxy={
            'http':ip
        }
        time.sleep(1)
        print(requests.get('https://api.bilibili.com/x/relation/followings?vmid=61382499&pn=1&ps=20&order=desc&jsonp=jsonp&callback=__jp3',headers=headers,proxies=proxy).text)
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-agent='+ua)
        chrome_options.add_argument('--proxy-server=http://'+ip)

        browser = webdriver.Chrome(chrome_options=chrome_options,executable_path='D:\soft\develop\chromedriver_win32\chromedriver.exe')
        try:
            browser.get('https://space.bilibili.com/492946185/fans/follow')
            time.sleep(4)
            print(browser.find_elements_by_css_selector('.be-pager-total')[0].text)
            print(browser.get_cookies())
            ava_ips.append(ip)
            print('可用ip：{0}'.format(ip))
        except Exception as e:
            print(browser.get_cookies())
            print("不可用ip:{0}".format(ip))
            # break
        
        # if resp.status_code==requests.codes.ok:
        #     ava_ips.append(ip)
        #     print('可用ip：{0}'.format(ip))
            
            

if __name__ == '__main__':
    # 可用ip
    ava_ips=[]
    ips = doRequest(2)
    filterAvailableIps(ips,ava_ips)
    print(ava_ips)

    # 记录可用ip
    with open('bilibili-spider\\ip-pool.txt','a') as f:
        for ip in ava_ips:
            f.write(ip)
            f.write('\r')


