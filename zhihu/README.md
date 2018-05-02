## 最新知乎模拟登录

- 登录接口改为:https://www.zhihu.com/api/v3/oauth/sign_in 

- 动态表单参数signature是多个变量进行hmac sha1 hash得到的一个值
对应的参数:clientId，grantType，source都是不变的,只有timestamp是
变化的,自定义一个.

- 验证码接口https://www.zhihu.com/api/v3/oauth/captcha?lang=en
en是普通验证码
