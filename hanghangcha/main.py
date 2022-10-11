import base64
import json
import re

import requests
from Crypto.Cipher import AES


def aes_decrypt(b64_text: str, key: str):
    key = key.encode()
    cipher = AES.new(key, mode=AES.MODE_ECB)
    text = base64.b64decode(b64_text)
    raw_text = cipher.decrypt(text).decode()
    text = re.sub("[\x00-\x09|\x0b-\x0c|\x0e-\x1f]", "", raw_text)
    return json.loads(text)


url = "https://api.hanghangcha.com/hhc/tag"
r = requests.get(url)
print(aes_decrypt(r.json()["data"], "3sd&d24h@$udD2s*"))
