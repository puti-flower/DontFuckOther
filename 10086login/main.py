import base64
import sys
import time

import requests

sys.path.append(".")
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from tools.convert import text_to_dict


def encrypt(text: str) -> str:
    sign_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsgDq4OqxuEisnk2F0EJFmw4xKa5IrcqEYHvqxPs2CHEg2kolhfWA2SjNuGAHxyDDE5MLtOvzuXjBx/5YJtc9zj2xR/0moesS+Vi/xtG1tkVaTCba+TV+Y5C61iyr3FGqr+KOD4/XECu0Xky1W9ZmmaFADmZi7+6gO9wjgVpU9aLcBcw/loHOeJrCqjp7pA98hRJRY+MML8MK15mnC4ebooOva+mJlstW6t/1lghR8WNV8cocxgcHHuXBxgns2MlACQbSdJ8c6Z3RQeRZBzyjfey6JCCfbEKouVrWIUuPphBL3OANfgp0B+QG31bapvePTfXU48TYK0M5kE+8LgbbWQIDAQAB"
    rsa_key = RSA.import_key(base64.b64decode(sign_key))
    cipher = PKCS1_v1_5.new(rsa_key)
    return base64.b64encode(cipher.encrypt(text.encode())).decode()


url = "https://login.10086.cn/login.htm"
data = text_to_dict(
    f"""
    accountType: 02
    pwdType: 03
    account: {encrypt("123123@qq.com")}
    password: {encrypt("dddddssz")}
    inputCode: e8m37n
    backUrl: https://touch.10086.cn/i/
    rememberMe: 0
    channelID: 12014
    protocol: https:
    loginMode: 03
    timestamp: {int(time.time() * 1000)}
    """
)


# https://login.10086.cn/captchazh.htm?type=03&timestamp=1665471877923
# 生成CaptchaCode rdmdmd5 captchatype

# https://login.10086.cn/loadSendflag.htm?timestamp=
# 生成sendflag
headers = text_to_dict(
    """
    Accept: application/json, text/javascript, */*; q=0.01
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
    Cache-Control: no-cache
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Cookie: sendflag=20221011150352915384; CaptchaCode=BSreZK; rdmdmd5=DD03D33020CFB2180F8EC11C0850E0FE
    Host: login.10086.cn
    Origin: https://login.10086.cn
    Pragma: no-cache
    Referer: https://login.10086.cn/html/login/email_login.html
    sec-ch-ua: "Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-origin
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37
    X-Requested-With: XMLHttpRequest
    """
)

r = requests.post(url, data=data, headers=headers)
print(r.text)
