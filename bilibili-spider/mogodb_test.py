import pymongo as pm
import requests
import json

# client = pm.MongoClient('localhost',27017)

# if 'biliUsers' in client.list_database_names():
#     print('bilibili用户库已存在')
# else:
#     # 创建db
#     bilibili_user_db = client['biliUsers']
        
# # 创建集合 类似于mysql的表
# if 'userInfo' in bilibili_user_db.list_collection_names():
#     print('bilibili用户集合已存在')
# else:
#     bilibili_user_db = client['biliUsers']
#     user_table = bilibili_user_db['userInfo']

# user_table = bilibili_user_db.['userInfo']

proxy={
    'http':'60.182.21.237:9000'
    # 'http':'61.161.27.35:9999',
    # 'http':'110.243.18.15:9999',
    # 'http':'60.169.134.247:9999'
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


user_sta_url = 'https://space.bilibili.com/25105113/fans/follow'

# user_stat = json.loads(requests.get(user_sta_url.format('25105113'),headers=headers,proxies=proxy).text)
user_stat = requests.get(user_sta_url.format('25105113'),headers=headers,proxies=proxy).text

print(user_stat)



# db = client.test



# post = {
#         "id": "111111",
#         "level": "MVP",
#         "real":1,
#         "profile": '111',
#         'thumb':'2222',
#         'nikename':'222',
#         'follows':20
# }

# db.col.insert_one(post) # 插入单个文档

# print(db.col.find_one())
