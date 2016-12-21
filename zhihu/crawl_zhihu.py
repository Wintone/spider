#!/usr/bin/python
# -*- coding:utf-8 -*-
import gzip
import re
import http.cookiejar
import urllib.request
import urllib.parse
import ssl 
import time
from PIL import Image
 
def ungzip(data):
    try:        
        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data
 
def getXSRF(data):
    cer = re.compile(r'<input type="hidden" name="_xsrf" value="(.*?)"')
    strlist = cer.findall(data)
    return strlist[0]
 
def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
 
def get_captcha():
    """
    获取验证码本地显示
    返回你输入的验证码
    """
    t = str(int(time.time() * 1000))
    # 验证码完整网址
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    # 下载验证码图片，用下面注释掉的方法一样的效果
    #urllib.request.urlretrieve(captcha_url, 'cptcha.gif')
    image_data = opener.open(captcha_url).read()
    with open('cptcha.gif', 'wb') as f:
        f.write(image_data)
    #用Pillow库显示图片，免去手动去文件夹打开的麻烦
    im = Image.open('cptcha.gif')
    im.show()
    captcha = input('本次登录需要输入验证码： ')
    return captcha

header = {
    'Host': 'www.zhihu.com',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

try:  
    _create_unverified_https_context = ssl._create_unverified_context  
except AttributeError:  
    # Legacy Python that doesn't verify HTTPS certificates by default  
    pass  
else:  
    # Handle target environment that doesn't support HTTPS verification  
    ssl._create_default_https_context = _create_unverified_https_context  
 
url = 'https://www.zhihu.com/'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
data = ungzip(data)     # 解压
#print(data)
_xsrf = getXSRF(data.decode('utf-8'))
 
url += 'login/email'
id = '609042866@qq.com'
password = '6994116'
postDict = {
        '_xsrf':_xsrf,
        'email':id,
        'password':password,
        'remember_me':'true'
}
postDict['captcha'] = get_captcha()
postData = urllib.parse.urlencode(postDict).encode('utf-8')
op = opener.open(url, postData)
data = op.read()
data = ungzip(data)
 
print(data.decode())