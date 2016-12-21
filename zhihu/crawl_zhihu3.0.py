import re
import requests
import http.cookiejar
from PIL import Image
import time
import json
import ssl

headers = {'User-Agent':'Mozilla5.0 (Windows NT 6.1; Win64; x64; rv48.0) Gecko20100101 Firefox48.0'}
filename = 'cookie'

# 建立一个会话，可以把同一用户的不同请求联系起来；直到会话结束都会自动处理cookies
'''
requests.Session()或者requests.session()，大小写一样的，我也不知道这样有啥区别。
看类型都是一个class 'requests.sessions.Session'这样的类。
requests.Session()会新建一个会话，可以把同一用户的不同请求联系起来，
直到会话结束都会自动处理cookies，这比urllib方便多了。
如果只使用requests.get()或者requests.post()每次访问网页都是独立进行的，
并没有把当前用户的多次访问关联起来，故而模拟登录需要用到requests.Session()。
然后再用新建的session使用post()，get()等函数。如下。

session = requests.Session()
session.get(url, headers)
session.post(url, headers, data)

'''
session = requests.Session()
# 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件。
# 而MozillaCookieJar类是存为'.txt'格式的文件
session.cookies = http.cookiejar.LWPCookieJar(filename)
# 若本地有cookie则不用再post数据了
try:
    session.cookies.load(filename=filename, ignore_discard=True)
except:
    print('Cookie未加载！')


def get_xsrf():
    '''
    获取参数_xsrf
    '''
    
    response = session.get('https://www.zhihu.com', headers=headers, verify=False)
    html = response.text
    get_xsrf_pattern = re.compile(r'<input type="hidden" name="_xsrf" value="(.*?)"')
    _xsrf = re.findall(get_xsrf_pattern, html)[0]
    return _xsrf


def get_captcha():
    '''
    获取验证码本地显示
    返回你输入的验证码
    '''
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    response = session.get(captcha_url, headers=headers, verify=False)
    with open('cptcha.gif', 'wb') as f:
        f.write(response.content)
    # Pillow显示验证码
    im = Image.open('cptcha.gif')
    im.show()
    captcha = input('本次登录需要输入验证码： ')
    return captcha


def login(username, password):
    '''
    输入自己的账号密码，模拟登录知乎
    '''
    # 检测到11位数字则是手机登录
    if re.match(r'd{11}$', account):
        print('使用手机登录中...')
        url = 'http://www.zhihu.com/login/phone_num'
        data = {'_xsrf': get_xsrf(),
                'password': password,
                'remember_me' :'true',
                'phone_num' :username
                }
    else:
        print('使用邮箱登录中...')
        url = 'https://www.zhihu.com/login/email'
        data = {'_xsrf': get_xsrf(),
                'password': password,
                'remember_me': 'true',
                'email': username
                }
    '''
    # 若不用验证码，直接登录
    try:
        result = session.post(url, data=data, headers=headers)
        print((json.loads(result.text))['msg'])
    # 要用验证码，post后登录
    except:
    '''
    data['captcha'] = get_captcha()
    result = session.post(url, data=data, headers=headers, verify=False)
    print((json.loads(result.text))['msg'])
    # 保存cookie到本地
    session.cookies.save(ignore_discard=True, ignore_expires=True)


if __name__ == '__main__':
    #account = input('输入账号：')
    #secret = input('输入密码：')
    account = '609042866@qq.com'
    secret = '6994116'
    login(account, secret)


    # 设置里面的简介页面，登录后才能查看。以此来验证确实登录成功
    get_url = 'https://www.zhihu.com/settings/profile'
    # allow_redirects=False 禁止重定向
    resp = session.get(get_url, headers=headers, allow_redirects=False)
    print(resp.text)
