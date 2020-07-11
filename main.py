from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import yagmail
from re import compile


def send_email(_user, _password, _host, _email, _contents):
    yag = yagmail.SMTP(user=_user, password=_password, host=_host)
    send_contents = _contents + '\n\n\npowered by fox2020.cn'
    yag.send(_email, 'SUES_News_Update', send_contents)
    print('Sent successfully')
    print('from %s to %s' % (_user, _email))


def ge_spider():
    url = 'https://ge.sues.edu.cn/19716/list.htm'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    response = get(url, headers={'User-Agent': ua})
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    s = soup.findAll('li', class_=compile(r"news n(\d) clearfix"))
    for item in s:
        title = '★' + item.find('a', href=compile(r'(\w)'))['title'] + '★'
        s_link = item.find('a', href=compile(r'(\w)'))['href']
        link = urljoin(url, s_link)
        date = item.find('span', class_="news_meta").text
        news = title + '\n' + link + '\n' + date
        ge_news = archive(title, news)
        return ge_news


def school_spider():
    url = 'https://www.sues.edu.cn/xxyw/list.htm'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    response = get(url, headers={'User-Agent': ua})
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    s = soup.findAll('a', class_=compile(r"column-news-item item-(.?) clearfix"))
    for item in s:
        title = item.find('span', class_='column-news-title').text
        link = urljoin(url, item['href'])
        date = item.find('span', class_='column-news-date news-date-hide').text
        news = title + '\n' + link + '\n' + date
        school_news = archive(title, news)
        return school_news


def archive(title, news):
    file = open(r'News_Archive.txt', 'r+', encoding='utf-8')
    if title in file.read():
        pass
    else:
        file.seek(0, 0)
        content = file.read()
        file.seek(0, 0)
        file.write(news + '\n' + '-' * 100 + '\n' + content)
        if send:
            send_email(_user, _password, _host, _email, news)
        return title
    file.close()


def run(i):
    counter = 0
    while True:
        counter += 1
        print('NO.' + str(counter) + '-' * 3 + time.strftime("%m/%d/%Y %H:%M"))
        s = school_spider()
        g = ge_spider()
        if s is not None:
            print('school news:', s)
        if g is not None:
            print('graduate news:', g)
        if s is None and g is None:
            print('No Update')
        time.sleep(i)


if __name__ == '__main__':
    send = False
    update = None
    need_mail = input('do you send a email?(Y/N)\n')
    interval = input('every interval time (unit:s)\n')
    if need_mail == 'y' or need_mail == 'Y':
        send = True
        print('Email Information Setting(*all mail services are supposed)')
        # you can change the following values with '_' to immutable strings
        # according to your information.
        _user = input('From>>>(mail address: eg:xxxxxxxxx@sues.edu.cn)\n')
        _password = input('mail password\n')
        _host = input('email host(SUES school mail STMP: smtphz.qiye.163.com)\n')
        _email = input('>>>To(mail address: eg:xxxxxx@gmail.com)\n')
        print('*' * 5, 'from', _user, '>>>', 'to', _email, '*' * 5)
        run(int(interval))
    else:
        run(int(interval))
