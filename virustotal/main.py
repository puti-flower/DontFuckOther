import execjs
import requests
import sys

sys.path.append(".")
from tools.convert import headers_to_dict

url = "https://www.virustotal.com/ui/search"
params = {"limit": 20, "relationships%5Bcomment%5D": "author%2Citem", "query": "hello"}


headers = headers_to_dict(
    """
    accept: application/json
    accept-encoding: gzip, deflate, br
    accept-ianguage: en-US,en;q=0.9,es;q=0.8
    accept-language: zh-CN,zh;q=0.9
    content-type: application/json
    referer: https://www.virustotal.com/
    sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    sec-fetch-dest: empty
    sec-fetch-mode: cors
    sec-fetch-site: same-origin
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36
    x-app-version: v1x123x1
    x-tool: vt-ui-main
    """
)

# 生成 x-vt-anti-abuse-header
# 网页使用的是btoa但是execjs 尽量使用Buffer.from
call_js = """
    function anti (){
                    const e = Date.now() / 1e3;
                    return Buffer.from((`${(()=>{
                        const e = 1e10 * (1 + Math.random() % 5e4);
                        return e < 50 ? "-1" : e.toFixed(0)
                    }
                    )()}-ZG9udCBiZSBldmls-${e}`)).toString('base64');
                }
"""
call_js = """
    function anti (){
                    const e = Date.now() / 1e3;
                    return btoa(`${(()=>{
                        const e = 1e10 * (1 + Math.random() % 5e4);
                        return e < 50 ? "-1" : e.toFixed(0)
                    }
                    )()}-ZG9udCBiZSBldmls-${e}`);
                }
"""
js = execjs.compile(call_js)
headers["x-vt-anti-abuse-header"] = js.call("anti")
r = requests.get(url, params=params, headers=headers)
print(r.json())
