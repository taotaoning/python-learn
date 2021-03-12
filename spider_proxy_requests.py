import requests
import random
import re
from bs4 import BeautifulSoup
import time
import os
import sys


# 免费代理ip地址
proxy_url='http://www.xiladaili.com/gaoni/{0}/'




# 读取头信息文件
def getUserAget():
    list_agents=[]
    with open('bilibili-spider\\user_agents.txt','r') as agents:
        for ua in agents.readlines():
            list_agents.append(ua.strip())
        return list_agents

# 请求代理网址，目前爬取指定页数进行挑选
def doRequest(pages):
    list_proxy_ips=[]
    uas = getUserAget()


    for item in range(1,pages):
        # 中间暂停2秒钟，避免请求频率过高
        time.sleep(2)
        ua=random.choice(uas)
        # 请求头
        headers={
            'User-Agent':ua,
            'Referer':'http://www.xiladaili.com/'
        }
        try:
            doReuestProxy(item,list_proxy_ips,headers)
        except Exception as e:
            print("获取当前页面代理ip数据失败：{1},{0}".format(e,item))

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
            'origin':'http://icanhazip.com',
            'Referer':'http://icanhazip.com'
        }

        proxy={
            'http': 'http://'+ip
        }

        try:
            # 避免请求频率过高
            time.sleep(1)
            #  http://icanhazip.com 检查代理是否成功网址
            response=requests.get("http://icanhazip.com",headers=headers,proxies=proxy)

            # resp=requests.get('https://api.bilibili.com/x/relation/followings?vmid=61382499&pn=1&ps=20&order=desc&jsonp=jsonp&callback=__jp3',headers=headers,proxies=proxy)

            if response.status_code==requests.codes.ok:
                print('可用ip：{0}'.format(ip))
                # response=requests.get("http://icanhazip.com",headers=headers,proxies=proxy)
                print(response.text)
                ava_ips.append(ip)

        except Exception as e:
            print(e)
            print("不可用ip:{0}".format(ip))
    
        # 记录可用ip
    with open('bilibili-spider\\ip-pool.txt','a') as f:
        for ip in ava_ips:
            f.write(ip)
            f.write('\r')

            
def getProxyIps():
    proxy_ips = []
    with open('bilibili-spider\\ip-pool.txt','r') as fil:
        for ipd in fil.readlines():
            content = ipd.strip();
            proxy_ips.append(content)
    return proxy_ips

if __name__ == '__main__':
    # 可用ip
    ava_ips=[]
    ips = doRequest(2)
    filterAvailableIps(ips,ava_ips)
    # print(ava_ips)

    print(getProxyIps())




