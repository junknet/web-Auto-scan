import aiohttp
import asyncio

page = 30

post_data = {
    'page': 1,
    'pageSize': 10,
    'keyWord': '',
    'dpIds': '',
}

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "34",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "secure; JSESSIONID=8NGWetn7NWF7Hb-SSkrbbzGDbYQzmNM_gjKj8wql4PXn2uc7ruv0!-96282387; __jsluid=72f938f1aa890b0ab98d726eb9d7d36f; Hm_lvt_606ad402d71f074871f1daa788ba943d=1557302782; Hm_lpvt_606ad402d71f074871f1daa788ba943d=1557302788",
    "Host": "credit.chaozhou.gov.cn",
    "Origin": "http://credit.chaozhou.gov.cn",
    "Referer": "http: // credit.chaozhou.gov.cn / ... ot % 3B,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

result = []


async def fetch(session, url, data):
    async with session.post(url=url, data=data, headers=headers) as response:
        return await response.json()


async def parse(html):
    xzcf_list = html.get('newtxzcfList')
    if xzcf_list is None:
        return
    for i in xzcf_list:
        result.append(i)


async def downlod(page):
    data = post_data.copy()
    data['page'] = page
    url = 'http://credit.chaozhou.gov.cn/tfieldTypeActionJson!initXzcfListnew.do'
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url, data)
        await parse(html)

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(downlod(i)) for i in range(1, page)]
tasks = asyncio.gather(*tasks)
# print(tasks)
loop.run_until_complete(tasks)
# loop.close()
# print(result)
count = 0
for i in result:
    print(i.get('cfXdrMc'))
    count += 1
print(f'total {count}')
