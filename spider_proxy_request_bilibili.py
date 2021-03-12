import requests
import re
import time
from bs4 import BeautifulSoup
import spider_proxy_requests as ips
import random
import pymongo
import json

#  定义全局信息

# 1.读取请求头
userAgents = ips.getUserAget()

ua = random.choice(userAgents)

# 2. 请求头信息，更换user-agent防止被禁
header={
    'user-agent':ua,
    'Referer':'https://space.bilibili.com'
}

# 3. 获取代理ip
proxyIps = ips.getProxyIps()

pi = random.choice(proxyIps)

proxy={
    'http': 'http://'+ pi
}

# 4.url
# 用户信息url
user_info_url = 'https://api.bilibili.com/x/space/acc/info?mid={0}&jsonp=jsonp'

user_sta_url = 'https://api.bilibili.com/x/relation/stat?vmid={0}&jsonp=jsonp'

# 关注列表url
following_url = 'https://api.bilibili.com/x/relation/followings?vmid={0}&pn={1}&ps=20&order=desc&jsonp=jsonp&callback=__jp3'

# 初始用户id
start_user_id = '25105113'

# 无密码连接mongodb
mongo_client = pymongo.MongoClient('127.0.0.1',27017)

# 连接指定db
biliUserDB = mongo_client.biliUsers

# 打印db下的所有集合
print(biliUserDB.collection_names)
# 连接聚集
biliUserTab = biliUserDB.userInfo

# 获取关注列表
def getFollows(userId):
    ua = random.choice(userAgents)
    pi = random.choice(proxyIps)
    
    time.sleep(2)
    resp = requests.get(following_url.format(userId,1),headers=header,proxies=proxy)

    if requests.codes.ok == resp.status_code:
        content = resp.text[6:-1]
        user_follows_resp = json.loads(content)['data']
        follows = user_follows_resp['list']
        if 0 == user_follows_resp['total']:
            return
        total_page = round(user_follows_resp['total'] / 20)

        for page_num in range(1,total_page+1):
            try:
                # 所关注人id
                follow_ids = []
                parseRespToList(follow_ids,userId,page_num,header,proxy)
                for fid in follow_ids:
                    # 首先检查是否已保存用户
                    find_condition = {
                        '_id' : fid,
                    }
                    find_result = biliUserTab.find_one(find_condition)
                    if None == find_result:
                        saveUserInfo(fid)
                    getFollows(fid)


            except Exception as e:
                print('获取当前用户：{0} 关注列表第{1}页失败：{2}'.format(userId,page_num,e))
    

# 解析请求关注列表相应信息保存关注列表id
def parseRespToList(follow_ids,userId,pageNum,header,proxy):

    ua = random.choice(userAgents)
    pi = random.choice(proxyIps)

    resp = requests.get(following_url.format(userId,pageNum),headers=header,proxies=proxy)

    if requests.codes.ok == resp.status_code:
        content = resp.text[6:-1]
        user_follows_resp = json.loads(content)
        follows = user_follows_resp['data']['list']

        # 保存第一页关注者id
        for follow in follows:
            follow_ids.append(follow['mid'])    


def saveUserInfo(userId):

    ua = random.choice(userAgents)
    pi = random.choice(proxyIps)

    time.sleep(2)
    resp = requests.get(user_info_url.format(userId),headers=header,proxies=proxy)

    time.sleep(2)
    ua = random.choice(userAgents)
    pi = random.choice(proxyIps)

    response = requests.get(user_sta_url.format(userId),headers=header,proxies=proxy)

    if requests.codes.ok == resp.status_code and requests.codes.ok == response.status_code:
        user_info = json.loads(resp.text)['data']
        user_sta = json.loads(response.text)['data']
        userInfo = {
            '_id': user_info['mid'],
            'birthday':user_info['birthday'],
            'coins':user_info['coins'],
            'faceUrl':user_info['face'],
            'level':user_info['level'],
            'name':user_info['name'],
            'sex':user_info['sex'],
            'sign':user_info['sign'],
            'follower':user_sta['follower'],
            'following':user_sta['following']
        }
        try:
            biliUserTab.insert_one(userInfo)
            print('保存用户信息：{0}',userInfo)
        except Exception as e:
            print('插入用户{0}信息失败：{1}'.format(userId,e))
    else:
        getFollows(userId)


if __name__ == '__main__':

    saveUserInfo(start_user_id)

    getFollows(start_user_id)



    