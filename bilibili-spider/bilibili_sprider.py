import requests
# import bs4

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium import ElementNotInteractableException
import urllib
import urllib3
import re
import time
from queue import Queue,LifoQueue,PriorityQueue

# 用户信息页面
user_info_url = 'https://space.bilibili.com/%s/fans/follow'


# 设置无头浏览器
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options,executable_path='D:\soft\develop\chromedriver_win32\chromedriver.exe')


# 选取一个用户 获取其信息
browser.get('https://space.bilibili.com/50329118/fans/follow')


# 获取关注页数
# pattern = re.compile()
page_total = browser.find_elements_by_css_selector('.be-pager-total')[0].text
page_total = int(re.search('\d+',page_total).group())
print(page_total)
for index in range(0,page_total):
    fork_names = browser.find_elements_by_css_selector('.vip-name-check.fans-name')
    for fork in fork_names:
        print(fork.text)
    try:
        next_page = browser.find_elements_by_css_selector('.be-pager-next')[0]
        next_page.click()
    except Exception:
        break;

    time.sleep(0.5)
    # 多个class选择


# 多个class选择
fork_names = browser.find_elements_by_css_selector('.vip-name-check.fans-name')
for fork in fork_names:
    print(fork.text)




def cycle_forks(fork_id,browser):
    fork_url = str.format(user_info_url,fork_id)
    browser.get(fork_url)

    try:
        page_total = browser.find_elements_by_css_selector('.be-pager-total')[0].text
        page_total = int(re.search('\d+',page_total).group())
    except Exception:
        return
    
    for index in range(0,page_total):
        fork_names = browser.find_elements_by_css_selector('.vip-name-check.fans-name')
        for fork in fork_names:
            print(fork.text)
        try:
            next_page = browser.find_elements_by_css_selector('.be-pager-next')[0]
            next_page.click()
        except Exception:
            break;







# cookies = dict(
#     _uuid='474950C2-9EC2-A4B5-BEBD-DC4D67D2A45137992infc',
#     blackside_state='1',
#     fingerprint='8dfdcc7a4d3717b76fd69c9b013b327',
#     sid='50329118',
#     DedeUserID='50329118',
#     CURRENT_FNVAL='80',
#      DedeUserID__ckMd5='50329118',
#     buvid3='5352B181-29D4-4101-8FB5-65D02B8F919A18549infc',
#     buvid_fp_plain='5352B181-29D4-4101-8FB5-65D02B8F919A18549infc',
#     PVID='12',
#     fingerprint3='a318682c183fc382c274fb22e5789b9',
#     fingerprint_s='d60abe48c7ed990c8e6f92997257177',
#     buvid_fp='5352B181-29D4-4101-8FB5-65D02B8F919A18549infc',
#     bfe_id='6f285c892d9d3c1f8f020adad8bed55'


# )

headers = {
    'origin':'https://space.bilibili.com',
    'referer':'https://space.bilibili.com/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    # 'cookies':'CURRENT_FNVAL=80; _uuid=474950C2-9EC2-A4B5-BEBD-DC4D67D2A45137992infoc; blackside_state=1; fingerprint=8dfdcc7a4d3717b76fd69c9b013b3227; SESSDATA=8dbe56a3%2C1630739065%2Cdfe33%2A31; bili_jct=310a0768f441e53578f5426ab25f9908; DedeUserID=25105113; DedeUserID__ckMd5=ec5e3dafa433c207; sid=i4k1nhek; buvid3=5352B181-29D4-4101-8FB5-65D02B8F919A18549infoc; PVID=12; fingerprint3=a318682c183fc382c274fb22e5789b9f; fingerprint_s=d60abe48c7ed990c8e6f929972571787; buvid_fp=5352B181-29D4-4101-8FB5-65D02B8F919A18549infoc; buvid_fp_plain=5352B181-29D4-4101-8FB5-65D02B8F919A18549infoc; bfe_id=6f285c892d9d3c1f8f020adad8bed553'
}

# print(requests.get('https://api.bilibili.com/x/member/web/login/log?jsonp=jsonp',headers=headers,cookies=cookies).content)

# print(requests.get('https://api.bilibili.com/x/space/acc/info?mid=25105113&jsonp=jsonp',headers).text)

# print(requests.get('https://space.bilibili.com/50329118/fans/follow',headers).text)

