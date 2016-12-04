# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2
import re
from furl import furl

class producer(object):
    # def __init__(self):
    #     self.db = MySQLdb.connect(
    #         host='192.168.1.22',
    #         port = 3306,
    #         user='root',
    #         passwd='asd123',
    #         db ='FAII',
    #         charset='utf8'
    #         )
    #     self.cursor=self.db.cursor()
    def in_url(self):


    def url(self):
        baseurl="http://www.baidu.com/"
        url=furl(baseurl).origin
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        pattern = re.compile(r'charset=([^\'\"]*?)[\'\"/\s]*?>')
        items = pattern.findall(html)
        if items:
            encode = items[0].replace('"', '').replace("'", '')
        if encode=="gb2312":
            html = html.decode("gb2312", "ignore").encode("utf-8", "ignore")
        gongan_url=self.getnum(html)
        if not gongan_url=='':
            return gongan_url
        else:
            bsObj = BeautifulSoup(html,'lxml')
            scripts=bsObj.findAll('script')
            for script in scripts:
                if 'src' in script.attrs:
                    href=script['src']
                    js_url=url+href
                    try:
                        js=requests.get(js_url)
                    except Exception,e:
                        print e
                        continue
                    js_conent=js.content
                    gongan_url=self.getnum(js_conent)
                    if not gongan_url=='':
                        return gongan_url

            print "此网站不合法"

    def getnum(self,html):
        b=re.findall('公\){0,1}.{0,2}备\s?([0-9]{9,15})|公网安备\s?([0-9]{9,15})',html)
        c=len(b)
        if c >0:
            for b1 in b[0]:
                if not b1=='':
                    url_gongan='http://www.beian.gov.cn/portal/registerSystemInfo?recordcode='+b1
                    return self.gongan(url_gongan)
        else:
            return ''

    def gongan(self,url_gongan):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url_gongan, headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        bsObj = BeautifulSoup(html,'lxml')
        gwablist=[]
        if bsObj.find('div',{"class":"p_cont"}):
            b=bsObj.find('div',attrs={'class':'p_cont'})
            c=b.findAll('td')
            for i in range(0,15,2):
                print c[i].text+":"+c[i+1].text
                gwablist.append(c[i].text.replace('"','').strip()+":"+c[i+1].text.replace('"','').strip())
            return gwablist
        else:
            return '没有找到信息'
if __name__ == '__main__':
    producer=producer()
    print producer.url()
