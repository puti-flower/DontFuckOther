import re
import sys

import execjs
import requests

sys.path.append(".")
from tools.convert import text_to_dict

# 由于jsl需要多次请求，所以要同一个会话
session = requests.Session()
session.headers = text_to_dict(
    """
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Connection: keep-alive
    Host: www.cnvd.org.cn
    Referer: https://www.cnvd.org.cn/patchInfo/list
    sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    Sec-Fetch-Dest: document
    Sec-Fetch-Mode: navigate
    Sec-Fetch-Site: same-origin
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36
    """
)

url = "https://www.cnvd.org.cn/flaw/list"


# 第一次请求 生成第一个cookie并且获取下一个cookie需要的参数
# 获取生成的cookie
r = session.get(url)
cookie_js = r.text.split("<script>document.cookie=")[-1].split(";location")[0]
jsl_k, jsl_v = execjs.eval(cookie_js).split(";")[0].split("=")
print(jsl_k, jsl_v)
session.cookies[jsl_k] = jsl_v

# 第二次请求，获取运行需要的参数
with open("cnvd/ob_md5.js", "r", encoding="utf-8") as f:
    call_clearance = execjs.compile(f.read())

r = session.get(url)
text = r.text
# 需要用到的数据
go_data = re.search(";go\((.*?)\)</script>", text).group(1)
# 加密的方式, 目前抓了几个包只有md5,那就只做md5的
sign_method = re.search('"ha":"(.*?)",', go_data).group(1)
jsl_k, jsl_v = call_clearance.eval(f"go({go_data})").split(";")[0].split("=")
session.cookies[jsl_k] = jsl_v

# 请求一下指定数据
url = "https://www.cnvd.org.cn/flaw/list?flag=true"
data = text_to_dict(
    """
    number: CNVD-2022-68075
    startDate: 
    endDate: 
    field: 
    order: 
    """
)
r = session.post(url, data=data)
print(r.text)
