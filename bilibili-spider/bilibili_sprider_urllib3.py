import urllib
import urllib3

http = urllib3.PoolManager(num_pools=50,timeout=3.0)

resp = http.request('GET','https://space.bilibili.com/50329118/fans/follow')

print(resp.data)
headers = {
    'origin':'https://space.bilibili.com',
    'referer':'https://space.bilibili.com/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

# print(requests.get('https://api.bilibili.com/x/space/acc/info?mid=25105113&jsonp=jsonp',headers).text)

# print(requests.get('https://space.bilibili.com/50329118/fans/follow',headers).text)

