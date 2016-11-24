#coding=utf-8
"""
author:xuxuerui
editor:luyao
"""
import os
import re
import sys
import json
import string
import pickle
import logging
import urllib2
import urlparse
import time
from bs4 import BeautifulSoup
import urllib 
reload(sys)
sys.setdefaultencoding('utf8')


import ly_work

my_skip_list=[]

class chicago(ly_work.GeneralCrawler):
    """
    chicago
    """
    def do_diff(self):
        self.skip_list=my_skip_list
        self.volume_flag = False
        self.sci_flag = False

    def __init__(self):
        ly_work.GeneralCrawler.__init__(self)
        
        self.do_diff()

        if not os.path.exists(self.__class__.__name__):
            os.mkdir(self.__class__.__name__)
        pass
    
    def _url_crawl_one(self, url, timeout=70):
        request = urllib2.Request(url)
        #httpHandler = urllib2.HTTPHandler(debuglevel=1)
        #httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        #res = urllib2.urlopen(url, timeout=timeout)
        #opener = urllib2.build_opener(httpHandler, httpsHandler)
        #urllib2.install_opener(opener)
        #request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
        #request.add_header('Connection', 'keep-alive')
        request.add_header('cookie', 'I2KBRCK=1')
        res = urllib2.urlopen(request, timeout=timeout)
        return res

    def _original_set(self):
        self.original_url = 'http://www.journals.uchicago.edu/action/showPublications?alphabetRange=&pageSize=20&startPage='
        pass

    def _original_analy(self, url, res):
        soup = BeautifulSoup(res, "lxml")
        u=soup.find('ul',{'class':'linkList centered'})
        assert u
        self.page_num=0
        for l in u.findAll('li',{'class':'pageLinks'}):
            self.page_num +=1
        
        logging.debug('get %d pages!' % (self.page_num))
        return True

    def _home_page_iter(self):
        prefix='http://www.journals.uchicago.edu/action/showPublications?alphabetRange=&pageSize=20&startPage='
        for s in range(0, self.page_num):
            index=str(s)
            yield prefix+index

    def _home_analy(self, url, res):
        soup = BeautifulSoup(res, "lxml")
        t=soup.find('tbody')
        assert t
        ans = []
        for td in t.findAll('td'):
            if td.find('img'):
                continue
            link = td.find('a')['href'].encode('utf8')
            link = urlparse.urljoin(url, link)
            journal_name = td.find('a').text.encode('utf8')
            logging.debug('get journal %s %s' % (link, journal_name))
            ans.append([link, journal_name])
        
        self.home_list.append([url, ans])
        return True

    def _year_page_iter(self):
        total=len(self.home_list)
        count=0
        prefix ='http://www.journals.uchicago.edu/loi/'
        for data1 in self.home_list:
            count+=1
            logging.debug('Completion : %d/%d' % (count,total))
            for url, name in data1[1]:
                site=url.split('/')[-2]
                link=prefix+site
                logging.debug('get year page %s' % link)
                yield link, name

    def _year_analy(self, url, res):
        soup = BeautifulSoup(res, "lxml") 
        l = soup.find('article', {'class':'decade-list volume-list'})
        ans = []
        if l: 
            for years in l.findAll('div',{'class':'expandable years'}):
                for a in years.findAll('a',{'class':'expander'}):
                    year=a.text.encode('utf8')
                    volume = ''
                    link='####'.join([url,year])
                    ans.append([year, volume, link])
        else:
            assert False,'no vlist'
        self.year_list.append(ans)
        return True

    def _year_check_better(self, name, new_url, old_url):
        tag_list=[]
        flag=False
        raise Exception('different url to one journal'), name
    
    def _issue_analy(self, url, year, res):
        soup = BeautifulSoup(res, "lxml") 
        l = soup.find('article', {'class':'decade-list volume-list'})
        ans = []
        has_result = False
        if l: 
            for years in l.findAll('div',{'class':'expandable years'}):
                for div in years.findAll('div'):
                    a=div.find('a',{'class':'expander'})
                    if a and year==a.text.encode('utf8'):
                        for i in div.findAll('div',{'class':'expandable issues'}):
                            im=i.find('span',{'class':'issueMeta'})
                            assert im,'no issue meta!'
                            link=im.a['href'].encode('utf8')
                            vol=im.a.text.encode('utf8').strip().replace('  ','').replace('\n','')
                            issue=vol
                            ans.append([link, issue,'','',vol])
                            logging.debug('get issue link  %s' % link)
                            has_result = True
                        break
                if has_result:
                    break
        """ 
           if not has_result:
            ans.append('sb')
        """
        assert has_result,'no result!'
        self.issue_list.append(ans)
        return True

    def _issue_crawl(self, url_y):
        idx = 0
        url,year=url_y.split('####')[:2]
        logging.debug('split url_y into %s and %s' % (url, year))
        while idx < 5:
            logging.debug('to crawl url %s : try  %d th time' % (url, idx))
            res = None
            try:
                res = self._url_crawl_one(url)
                if res:
                    if self._issue_analy(url, year, res):
                        return res
                time.sleep(10)
            except Exception as e:
                logging.error('error in crawl and analy %s ' % repr(e))
                pass

            idx += 1
        return None
     
    def _issue_page_iter(self):
        total=len(self.year_list)
        count=0
        for journal in self.year_list:
            count+=1
            logging.debug('Completion : %d/%d' % (count,total))
            for vol in journal:
                yield vol[2], vol[3], vol[0], vol[1]

    
    def _atcpage_page_iter(self):
        total=len(self.issue_list)
        count=0
        for s in self.issue_list:
            count+=1
            logging.debug('Completion : %d/%d' % (count,total))
            for ss in s:
                yield ss[0]

    def _atcpage_analy(self, url, res):
        soup = BeautifulSoup(res, "lxml")
        if soup.find('div', {'class': 'toc'}):
            l = soup.find('span', {'class': 'number-of-pages'})
            if l:
                num = int(l.text.encode('utf8'))
            else:
                num =1
            logging.debug('get atcpage num %d' % (num))
            self.atcpage_num[url]=num
            return True 
        else:
            return False
    
    def _article_page_iter(self):
        total=len(self.issue_list)
        count=0
        for s in self.issue_list:
            count+=1
            logging.debug('Completion : %d/%d' % (count,total))

            for ss in s:
                yield ss[0], ss[2], ss[3], ss[1], ss[4]


    def _article_analy(self, url, res):
        if res == '5 timeout':
            self.article_list.append([])
            return True
        soup = BeautifulSoup(res, "lxml")
        ans = []
        has_result = False
        l = soup.find('form',{'name':'frmAbs'})
        if l:
            for ss in l.findAll('table',{'class':'articleEntry'}):
                t = ss.find('span',{'class':'hlFld-Title'})
                assert t, 'no title!'
                title = t.text.encode('utf8')
                
                link=''
                for a in ss.findAll('a'):
                    if a.previous_sibling and a.previous_sibling.text and\
                        (a.previous_sibling.text.encode('utf8') == 'Reviews' or 
                        a.previous_sibling.text.encode('utf8') == 'Book Reviews'):
                        break
                    if a.text.encode('utf8') == 'Full Text' or a.text.encode('utf8') == 'First Page'\
                        or 'Abstract' in a.text.encode('utf8') or 'PDF' in a.text.encode('utf8'):
                        link = a['href'].encode('utf8')
                        link = urlparse.urljoin(url, link)
                        break
               
                author=[]
                for authors in ss.findAll('span',{'class':'hlFld-ContribAuthor'}):
                    author.append(authors.text.encode('utf8'))
                
                page=''
                if ss.find('span',{'class':'articlePageRange'}):
                    page=ss.find('span',{'class':'articlePageRange'}).text.encode('utf8')

                logging.debug('article page analy get title : %s' % title)
                ans.append({'link':link, 'title':title, 'author_list':author, 'page':page})
                has_result = True
            """
            if not has_result:
                ans.append('sb')
                has_result = True
            """
        else:
            assert False,'no content'

        assert has_result, 'has_result'
        self.article_list.append(ans)
        return True
    pass
