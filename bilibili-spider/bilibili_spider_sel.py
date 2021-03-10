import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import urllib
import urllib3
import re
import time
import json
import pymongo as pm

# 用户关注用户页面
user_fans_url = 'https://space.bilibili.com/{0}/fans/follow'

# 用户信息接口
user_info_url = 'https://api.bilibili.com/x/space/acc/info?mid={0}&jsonp=jsonp'

# 用户关注信息接口
user_sta_url = 'https://api.bilibili.com/x/relation/stat?vmid={0}&jsonp=jsonp'

# 用户作品信息接口
user_upstat_url = 'https://api.bilibili.com/x/space/upstat?mid={0}&jsonp=jsonp'

proxy={
    'http':'118.212.143.43:3601',
    'http':'61.161.27.35:9999',
    'http':'110.243.18.15:9999',
    'http':'60.169.134.247:9999'
    # 'http':'36.250.156.53:9999',
    # 'http':'175.42.122.241:9999',
    # 'http':'49.70.85.149:9999',
    # 'http':'117.64.225.58:9999',
    # 'http':'175.43.57.12:9999',
}


headers = {
    'origin':'https://space.bilibili.com',
    'referer':'https://space.bilibili.com/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    # 'cookies':'CURRENT_FNVAL=80; _uuid=474950C2-9EC2-A4B5-BEBD-DC4D67D2A45137992infoc; blackside_state=1; fingerprint=8dfdcc7a4d3717b76fd69c9b013b3227; SESSDATA=8dbe56a3%2C1630739065%2Cdfe33%2A31; bili_jct=310a0768f441e53578f5426ab25f9908; DedeUserID=25105113; DedeUserID__ckMd5=ec5e3dafa433c207; sid=i4k1nhek; buvid3=5352B181-29D4-4101-8FB5-65D02B8F919A18549infoc; PVID=12; fingerprint3=a318682c183fc382c274fb22e5789b9f; fingerprint_s=d60abe48c7ed990c8e6f929972571787; buvid_fp=5352B181-29D4-4101-8FB5-65D02B8F919A18549infoc; buvid_fp_plain=5352B181-29D4-4101-8FB5-65D02B8F919A18549infoc; bfe_id=6f285c892d9d3c1f8f020adad8bed553'
}


selenium_proxy = '113.194.131.208:9999'
# proxy = new Proxy().setHttpProxy(proxyServer).set`SslProxy(proxyServer);

# 设置无头浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# chrome_options.setHttpProxy(selenium_proxy).setSslProxy(selenium_proxy)
chrome_options.add_argument(f'-proxy-server=http://220.174.236.211:8091')
browser = webdriver.Chrome(options=chrome_options,executable_path='D:\soft\develop\chromedriver_win32\chromedriver.exe')
browser.get('https://www.wanbianip.com/News-getInfo-id-644.html')
print(browser.page_source)

client = pm.MongoClient('localhost',27017)

if 'biliUsers' in client.list_database_names():
    print('bilibili用户库已存在')
else:
    # 创建db
    bilibili_user_db = client['biliUsers']

bilibili_user_db = client['biliUsers']

# 创建集合 类似于mysql的表
if 'userInfo' in bilibili_user_db.list_collection_names():
    print('bilibili用户集合已存在')
else:
    bilibili_user_db = client['biliUsers']
    user_table = bilibili_user_db['userInfo']

user_table = bilibili_user_db['userInfo']
# 创建索引
user_table.create_index('mid',unique=True)



def cycle_forks(fork_id,browser):
    fork_url = user_fans_url.format(fork_id)
    browser.get(fork_url)
    # 获取用户信息
    content = requests.get(user_info_url.format(fork_id),headers=headers).content
    user_info = json.loads(requests.get(user_info_url.format(fork_id),headers=headers,proxies=proxy).text)
    user_stat = json.loads(requests.get(user_sta_url.format(fork_id),headers=headers,proxies=proxy).text)
    user_upsta = json.loads(requests.get(user_upstat_url.format(fork_id),headers=headers,proxies=proxy).text)
    time.sleep(1)
    mongo_user = {
        'mid':user_info.mid,
        'name':user_info.name,
        'face':user_info.face,
        'level':user_info.level,
        'sex':user_info.sex
    }
    try:
        user_table.insert_one(mongo_user)
    except Exception as e:
        print("已存在用户：%s " % user_info.mid)
        return
    print(content)
    list_ids = []
    try:
        a_ids = browser.find_elements_by_css_selector('.cover')
        for item in a_ids:
            ls = item.get_attribute('href')
            a_id = re.findall('\d+',ls)[0]
            list_ids.append(a_id)
    except Exception as e:
        print(e)
        return


    try:
        page_total = browser.find_elements_by_css_selector('.be-pager-total')[0].text
        print(re.findall('\d+',page_total))
        page_total = int(re.findall('\d+',page_total)[0])
    except Exception as e:
        print(e)
        page_total = 1
        # return
    
    for index in range(0,page_total):
        fork_names = browser.find_elements_by_css_selector('.vip-name-check.fans-name')
        time.sleep(1)
        for item in fork_names:
            print(item.text)
        try:
            next_page = browser.find_elements_by_css_selector('.be-pager-next')[0]
            
            next_page.click()
            time.sleep(1)
        except Exception as e:
            print(e)
            break;
    for item in list_ids:
        cycle_forks(item,browser)


# cycle_forks('25105113',browser)