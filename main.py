import requests
from requests_html import HTML

url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
next_page = []
flag = True


# 向ptt網站提出GET請求
def get_request(url):
    response = requests.get(url, cookies={'over18': '1'})
    return response


# 取得html的內容
def get_content(doc, next_page):
    html = HTML(html=doc)
    contents = html.find('div.r-ent')
    c = html.find('.action-bar a.btn.wide')[1].attrs
    next_page.append('https://www.ptt.cc'+c['href'])
    return contents


# 處理資料
def process_data(content, r):  # title author date
    title = content.find('div.title', first=True).text
    nrec = content.find('div.nrec', first=True).text
    meta = content.find('div.meta', first=True)
    r['title'] = title
    r['nrec'] = nrec
    r['author'] = meta.find('div.author', first=True).text
    r['date'] = meta.find('div.date', first=True).text
    return r


resp = get_request(url)
contents = get_content(resp.text, next_page)
# 輸出第一頁的資料
for i in contents:
    result = {}
    process_data(i, result)
    print("%2s %2s %2s %2s" % (result["nrec"], result["title"], result["author"], result["date"]))
print('-'*50)
while flag:
    url = next_page[len(next_page)-1]
    if 'index1' in url:
        flag = False
    resp = get_request(url)
    contents = get_content(resp.text, next_page)
    for i in contents:
        result = {}
        process_data(i, result)
        print("%2s %2s %2s %2s" % (result["nrec"], result["title"], result["author"], result["date"]))
    print('-' * 50)

