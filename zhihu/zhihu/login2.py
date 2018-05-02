import requests
from bs4 import BeautifulSoup


cookie = 'q_c1=a034cbf4377a4acbb4699c9974be2f7e|1523271364000|1523271364000; _zap=88c891db-350b-4e71-9ec1-736e0f982529; __utmv=51854390.100--|2=registration_date=20160317=1^3=entry_date=20160317=1; aliyungf_tc=AQAAANZYEHYWfwoA9L7Hb6AVkAXiUvP2; _xsrf=3528909f-8cf0-4121-9e6a-b2ec848ce158; d_c0="ANCuLrO-dw2PTgS8HXJN85cpp_b-AZq6EH8=|1524154245"; __utmc=51854390; __utmz=51854390.1524154473.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; l_n_c=1; n_c=1; l_cap_id="ODFhODI1Y2E2NDYxNDdjMmE3NjFmY2VjNmY2MzhkYjc=|1524165439|f7d3e51b1185db73abea12680795ba4bd9949d68"; r_cap_id="Yjk3OGFkZmRjOWZhNDQ2NzkzNzhiNjgwMTg0NmFhMzU=|1524165439|36aa08ce0f0c49f22cea15db6e533c9563d74e48"; cap_id="ZDg1MzdiN2M3M2JhNGI0NTkzMGNjODgzY2FkMDY5M2M=|1524165439|6c51cbb3e00ab5b72826ef8ed421732723a05dcb"; __utma=51854390.2045526800.1523805076.1524154473.1524165459.4; __utmb=51854390.0.10.1524165459; capsion_ticket="2|1:0|10:1524167047|14:capsion_ticket|44:YmMyMDA2OTFlZWQ1NGQzZDlmMWI0Mzc2ODU5YTA5NWE=|28e71f30dbf60389f64fcf0cf3ca9c741421af68a288799e218c519c1024c153"'
headers = {
    'Host': 'www.zhihu.com',
    'Origin': 'https://www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'cookie': cookie
}

url = 'https://www.zhihu.com/people/hua-kai-hua-luo-21-3/activities'
res = requests.get(url, headers=headers)
html = BeautifulSoup(res.text, 'html.parser')
x = html.find_all('title')[0].string
print(x)
