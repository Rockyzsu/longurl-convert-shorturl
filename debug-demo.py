import requests

url='http://127.0.0.1:8081/shorten/'
data={'longurl':'https://www.amazon.com/dp/B0BRC3XDXH?m=A3S3U8R1861IDQ&th=1&keywords=SALESAHOLIC+FACEBOOK+GROUP&linkCode=sl1&tag=salesaholic-20&linkId=485ffa0dc149afba7a9a1fb8056a59e5&language=en_US&ref_=as_li_ss_tl'}
header={'content-type':'application/json'}
req = requests.post(url,json=data,headers=header)
print(req.text)