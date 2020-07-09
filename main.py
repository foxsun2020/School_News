from tkinter import *
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import yagmail


def send_email(contents):
    yag = yagmail.SMTP(user=v1.get(), password=v2.get(), host=v3.get())
    email = v4.get()
    send_contents = contents + '\n\n\npowered by fox2020.cn'
    yag.send(email, 'SUES_News_Update', send_contents)
    print('Send an Email to', v4.get())


def news_spider():
    state = False
    url = 'https://www.sues.edu.cn/xxyw/list.htm'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    response = get(url, headers={'User-Agent': ua})
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    for i in range(1, 14):
        html = 'column-news-item item-%s clearfix' % i
        node = soup.find('div', class_='column-news-con').find('a', class_=html)
        title = node.find('span', class_='column-news-title')
        data = node.find('span', class_='column-news-date news-date-hide')
        file = open(r'D:\python\Day16-20\data\sues.txt', 'r+', encoding='utf-8')
        news = title.text + '\n' + data.text + '\n' + urljoin(url, node['href'])
        if title.text in file.read():
            continue
        else:
            file.seek(0, 0)
            content = file.read()
            file.seek(0, 0)
            file.write(news + '\n' + '-' * 50 + '\n' + content)
            send_email(news)
            state = True
        file.close()
    if state:
        print(time.ctime(time.time())+':Received a update!')
        log = "insert", time.ctime(time.time())+':Received a update!'
    else:
        print(time.ctime(time.time())+':None')
        log = "insert", time.ctime(time.time())+':None!'
    return log


def run(interval):
    while True:
        news_spider()
        time.sleep(interval)


root = Tk()
root.title('School News Collector')
root.geometry('320x500')

Label(root, text='').grid(row=0, sticky=W)
Label(root, text='Sender Information', font=('Helvetica', '10', 'bold')).grid(row=1, sticky=W, columnspan=5)
Label(root, text='E-mail').grid(row=2, sticky=W)
Label(root, text='password').grid(row=3, sticky=W)
Label(root, text='host').grid(row=4, sticky=W)
Label(root, text='* all mail service is supposed').grid(row=5, sticky=W, columnspan=5)
Label(root, text='').grid(row=6, sticky=W)
Label(root, text='Recipient Information', font=('Helvetica', '10', 'bold')).grid(row=7, sticky=W, columnspan=5)
Label(root, text='E-mail').grid(row=8, sticky=W)
Label(root, text='').grid(row=9, sticky=W)
Label(root, text='Setting', font=('Helvetica', '10', 'bold')).grid(row=10, sticky=W, columnspan=5)
Label(root, text='interval\n(unit:s)').grid(row=11, sticky=W)
Label(root, text='').grid(row=12, sticky=W)
Label(root, text='-' * 70).grid(row=14, columnspan=5, sticky=W)
Label(root, text='fox2020.cn').grid(row=20, sticky=S)

v1 = StringVar()
v1.set('*Your Student ID*@sues.edu.cn')
v2 = StringVar()
v3 = StringVar()
v3.set('smtphz.qiye.163.com')
v4 = StringVar()

Entry(root, textvariable=v1, width=30).grid(row=2, column=1)
Entry(root, textvariable=v2, width=30, show="*").grid(row=3, column=1)
Entry(root, textvariable=v3, width=30).grid(row=4, column=1)
Entry(root, textvariable=v4, width=30).grid(row=8, column=1)
s1 = Scale(root, from_=60, to=3600, orient=HORIZONTAL, length=190)
s1.grid(row=11, column=1)
t1 = Text(root, width=42, height=8)
t1.grid(row=15, columnspan=5, sticky=W, padx=10, pady=5)


b1 = Button(root, text='Start', width=10, command=lambda: run(int(s1.get())))
b1.grid(row=13, sticky=W, padx=10, pady=5)
b2 = Button(root, text='Exit', width=10, command=root.quit())
b2.grid(row=13, column=1, sticky=E, padx=10, pady=5)


mainloop()