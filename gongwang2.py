# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2
import re
import MySQLdb
from furl import furl

import requests



class producer(object):
    def __init__(self):
        self.db = MySQLdb.connect(
            host='192.168.1.22',
            port = 3306,
            user='root',
            passwd='asd123',
            db ='FAII',
            charset='utf8'
            )
        self.cursor=self.db.cursor()



    def urlname(self):
        url_new=[]
        baseurl="http://www.baidu.com/sadasdasdasdasdasdasdasd.html"
        domain_url=furl(baseurl).host
        url1=domain_url.split(".")
        for u in range(1,len(url1)):
            url_new.append(url1[u])
        a = '.'
        url=a.join(url_new)

        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        headers = {'User-Agent': user_agent}
        r=requests.post('http://www.beian.gov.cn/portal/registerSystemInfo',data={'flag':'2','domainname':url,'inputPassword':'0106'},headers=headers)
        zz=r.content
        bsObj = BeautifulSoup(zz,'lxml')
        gwablist=[]
        if bsObj.find('div',{"class":"p_cont"}):
            b=bsObj.find('div',attrs={'class':'p_cont'})
            c=b.findAll('td')
            for i in range(0,15,2):
                print c[i].text+":"+c[i+1].text
                gwablist.append(c[i].text.replace('"','').strip()+":"+c[i+1].text.replace('"','').strip())
                a=gwablist
            return gwablist
            # {test1: c[1].text, c[2].text: c[3].text,c[4].text:c[5].text,c[6].text:c[7].text,c[8].text:c[9].text,c[10].text:c[11].text,c[12].text:c[13].text,c[14].text:c[15].text})
        else:
            return '没有找到信息'



if __name__ == '__main__':
    producer=producer()
    producer.urlname()