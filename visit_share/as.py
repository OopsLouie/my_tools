#! /usr/bin/python3

# requests lib ref:https://www.jb51.net/article/180450.htm

import requests


# global value
s = requests.Session()
login_url = "https://share.teraspek.cn/dologin.action"

login_from_data = {
    "os_username" : "luyi",
    "os_password" : "hcy19970303",
    "login" : "Log in",
    "os_destination" : ""
}

headers = {
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "zh-CN,zh;q=0.9",
    "Connection" : "keep-alive",
    "Cache-Control" : "max-age=0",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    "Content-Type" : "application/x-www-form-urlencoded",
    "Host" : "share.teraspek.cn",
    "Origin" : "https://share.teraspek.cn",
    "Referer" : "https://share.teraspek.cn/login.action",
}

res1 = s.post(login_url,data=login_from_data,headers=headers)
print(res1.status_code)
print(res1.ok)
print(res1.headers)
#print(res1.headers['Set-Cookie'].split(';')[0])

#exit(0)

headers = {
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "zh-CN,zh;q=0.9",
    "Connection" : "keep-alive",
#    "Cookie" : res1.headers['Set-Cookie'].split(';')[0],
    "Host" : "share.teraspek.cn",
    "Referer" : "https://share.teraspek.cn/",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    "Sec-Fetch-Dest" : "document",
    "Sec-Fetch-Mode" : "navigate",
    "Sec-Fetch-Site" : "same-origin",
    "Sec-Fetch-User" : "?1",
    "Upgrade-Insecure-Requests" : "1"
}
download_url = "https://share.teraspek.cn/users/viewmyprofile.action"
res2 = s.get(download_url, headers=headers)
print(res2.headers)
#print(res2.content.decode())

with open("output.txt","w") as f:
    f.write(str(res2.content.decode()))
