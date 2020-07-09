from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import yagmail


def send_email(contents):
    yag = yagmail.SMTP(user='XXX@sues.edu.cn', password='XXX', host='smtphz.qiye.163.com')  # sender information
    email = 'XXX@gmail.com'  # recipient (your email address)
    send_contents = contents + '\n\n\npowered by fox2020.cn'
    yag.send(email, 'SUES_News_Update', send_contents)
    print('Send an Email to', email)


def news_spider():
    state = False
    url = 'https://www.sues.edu.cn/xxyw/list.htm'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    response = get(url, headers={'User-Agent': ua})
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    for i in range(1, 14):
        html = 'column-news-item item-%s clearfix' % i
        node = soup.find('div', class_='column-news-con').find('a', class_=html)
        title = node.find('span', class_='column-news-title')
        data = node.find('span', class_='column-news-date news-date-hide')
        file = open(r'News_Archive.txt', 'r+', encoding='utf-8')  # set the path of News_Archive.txt
        if title.text in file.read():
            continue
        else:
            file.seek(0, 0)
            content = file.read()
            news = title.text + '\n' + data.text + '\n' + urljoin(url, node['href'])
            file.seek(0, 0)
            file.write(news + '\n' + '-' * 50 + '\n' + content)
            send_email(news)
            state = True
        file.close()
    if state:
        print(time.ctime(time.time()) + ':Received a update!')
    else:
        print(time.ctime(time.time()) + ':None')


while True:
    news_spider()
    time.sleep(60)  # set interval time, unit: second
