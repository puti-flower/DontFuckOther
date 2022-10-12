# virustotal

- 加密方式: Header参数`x-vt-anti-abuse-header`
- 解决方式: 直接全局搜索函数，直接运行



# 新榜

- 加密方式: body参数 `nonce`和`xyz`
- 解决方式： 全局搜索并复制，直接运行即可

# 行行查(接收数据解密)

- 加密方式：aes加密
- 解决方式：跟随调用栈取得aes密钥跟模式，用py实现解密


# 移动邮箱登录
- 加密方式：账号密码RSA加密，验证码识别
- 解决方式：取得rsa的密钥py实现加密，验证码可用ddddocr

# cnvd漏洞
- 加密方式：加速乐cookie
- 解决方式：模拟流程2次请求取得cookie
- 难点：cookie生成需要请求的js，带ob混肴不太好看

# 抖音弹幕RPC
- 加密方式：一堆乱七八糟的
- 解决方式：用浏览器rpc注入js ws返回

