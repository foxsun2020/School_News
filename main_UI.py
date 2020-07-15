from tkinter import *
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import yagmail
from re import compile


def send_email(contents):
    yag = yagmail.SMTP(user=v1.get(), password=v2.get(), host=v3.get())
    email = v4.get()
    send_contents = contents + '\n\n\npowered by fox2020.cn'
    yag.send(email, 'SUES_News_Update', send_contents)
    print('Send an Email to', v4.get())


def ge_spider():
    url = 'https://ge.sues.edu.cn/19716/list.htm'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    response = get(url, headers={'User-Agent': ua})
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    s = soup.findAll('li', class_=compile(r"news n(\d) clearfix"))
    for item in s:
        title = item.find('a', href=compile(r'(\w)'))['title']
        s_link = item.find('a', href=compile(r'(\w)'))['href']
        link = urljoin(url, s_link)
        date = item.find('span', class_="news_meta").text
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
        file.write(news + '\n' + '-'*100 + '\n' +content)
        send_email(news)
    file.close()


def school_spider():
    state = False
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
        archive(title, news)


def run(interval):
    while True:
        school_spider()
        ge_spider()
        time.sleep(interval)


root = Tk()
root.title('School News Collector')
root.geometry('320x350')

Label(root, text='').grid(row=0, sticky=W)
Label(root, text='From', font=('Helvetica', '10', 'bold')).grid(row=1, sticky=W, columnspan=5)
Label(root, text='E-mail').grid(row=2, sticky=W)
Label(root, text='password').grid(row=3, sticky=W)
Label(root, text='host').grid(row=4, sticky=W)
Label(root, text='* all mail services are supposed').grid(row=5, sticky=W, columnspan=5)
Label(root, text='').grid(row=6, sticky=W)
Label(root, text='To', font=('Helvetica', '10', 'bold')).grid(row=7, sticky=W, columnspan=5)
Label(root, text='E-mail').grid(row=8, sticky=W)
Label(root, text='').grid(row=9, sticky=W)
Label(root, text='Setting', font=('Helvetica', '10', 'bold')).grid(row=10, sticky=W, columnspan=5)
Label(root, text='interval\n(unit:s)').grid(row=11, sticky=W)
Label(root, text='').grid(row=12, sticky=W)
Label(root, text='----fox2020.cn----').grid(row=16, sticky=W, padx=100, columnspan=5)

v1 = StringVar()
v1.set('suesedu@aliyun.com')
v2 = StringVar()
v2.set('sues2020')
v3 = StringVar()
v3.set('smtp.aliyun.com')
v4 = StringVar()
v4.set('xxx@gmail.com')

Entry(root, textvariable=v1, width=30).grid(row=2, column=1)
Entry(root, textvariable=v2, width=30, show="*").grid(row=3, column=1)
Entry(root, textvariable=v3, width=30).grid(row=4, column=1)
Entry(root, textvariable=v4, width=30).grid(row=8, column=1)
s1 = Scale(root, from_=60, to=3600, orient=HORIZONTAL, length=190)
s1.grid(row=11, column=1)


b1 = Button(root, text='Start', width=10, command=lambda: run(int(s1.get())))
b1.grid(row=13, sticky=W, padx=10, pady=5)
b2 = Button(root, text='Exit', width=10, command=root.quit())
b2.grid(row=13, column=1, sticky=E, padx=10, pady=5)


mainloop()
