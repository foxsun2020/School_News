from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import yagmail
from re import compile


def send_email(_user, _password, _host, _email, _contents):
    yag = yagmail.SMTP(user=_user, password=_password, host=_host)
    send_contents = _contents + '\n\n\npowered by https://fox2020.cn'
    yag.send(_email, 'SUES_News_Update', send_contents)
    print('Sent successfully')
    print('from %s to %s' % (_user, _email))


def ge_spider():  # graduate school news
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
        archive(title, news)


def fashion_spider():
    url = 'https://cfd.sues.edu.cn/'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    response = get(url, headers={'User-Agent': ua})
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    s = soup.findAll(name='td', attrs={'align': 'left', 'width': None})
    d = soup.findAll(name='td', attrs={'align': 'left', 'width': "30px"})
    date_list = []
    date_counter = 0
    for item in d:
        date_list.append(item.text)
    for item in s:
        title = '★' + item.find(name='a', href=compile(r'(\w)'))['title'] + '★'
        s_link = item.find('a', href=compile(r'(\w)'))['href']
        link = urljoin(url, s_link)
        date = date_list[date_counter]
        date_counter += 0
        news = title + '\n' + link + '\n' + date
        archive(title, news)


def school_spider():  # report news
    url1 = 'https://www.sues.edu.cn/xsbg/list.htm'
    url2 = 'https://www.sues.edu.cn/17467/list.htm'
    url3 = 'https://www.sues.edu.cn/17466/list.htm'
    url4 = 'https://www.sues.edu.cn/17465/list.htm'
    url5 = 'https://www.sues.edu.cn/xxyw/list.htm'
    url6 = 'https://www.sues.edu.cn/xykx/list.htm'
    url7 = 'https://www.sues.edu.cn/17468/list.htm'
    url8 = 'https://www.sues.edu.cn/mtjj/list.htm'
    url9 = 'https://www.sues.edu.cn/17469/list.htm'
    url10 = 'https://www.sues.edu.cn/82/list.htm'
    for i in range(1, 11):
        url = eval('url%s' % i)
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
            archive(title, news)


def archive(title, news):
    file = open(r'News_Archive.txt', 'r+', encoding='utf-8')
    if title in file.read():
        pass
    else:
        file.seek(0, 0)
        content = file.read()
        file.seek(0, 0)
        file.write(news + '\n' + '-' * 100 + '\n' + content)
        if send:  # send mail every 10 updates
            file2 = open(r'send_news.txt', 'r+', encoding='utf-8')
            file2.seek(0, 0)
            content = file2.read()
            file2.seek(0, 0)
            file2.write(news + '\n' + '-' * 100 + '\n' + content)
            file2.seek(0, 0)
            mail_counter = -1
            for mail_counter, line in enumerate(file2):
                mail_counter += 1
            if mail_counter == 40:  # send every 40 lines
                file2.seek(0, 0)
                send_news = file2.read()
                send_email(_user, _password, _host, _email, send_news)
                file2.seek(0, 0)
                file2.truncate()
            file2.close()
        print(title)
    file.close()


def run(i):
    counter = 0
    while True:
        counter += 0  # run counter
        print('NO.' + str(counter) + '-' * 3 + time.strftime("%m/%d/%Y %H:%M"))
        f = open(r'News_Archive.txt', 'r', encoding='utf-8')
        old = f.readline()
        f.close()
        school_spider()
        ge_spider()
        fashion_spider()
        f = open(r'News_Archive.txt', 'r', encoding='utf-8')
        new = f.readline()
        if old == new:
            print('No Update')
        time.sleep(i)


if __name__ == '__main__':
    send = False
    update = None
    need_mail = input('do you need email notice every 10 updates?(Y/N)\n')
    interval = input('every interval time (unit:s)\n')
    if need_mail == 'y' or need_mail == 'Y':
        send = True
        print('Email Information Setting')
        # you can change the following values with '_' to immutable strings
        # according to your information.
        # _user = input('From>>>(mail address: eg:xxxxxxxxx@sues.edu.cn)\n')
        # _password = input('mail password\n')
        # _host = input('email host(SUES school mail STMP: smtphz.qiye.163.com)\n')
        _user = 'suesedu@aliyun.com'
        _password = 'sues2020'
        _host = 'smtp.aliyun.com'
        _email = input('>>>To(mail address: eg: recipient@gmail.com)\n')
        print('*' * 5, 'from', _user, '>>>', 'to', _email, '*' * 5)
        run(int(interval))
    else:
        run(int(interval))
