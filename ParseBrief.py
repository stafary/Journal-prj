# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:08:31 2016

@author: v_mahuanhuan
"""
import time
import urllib2
import urlparse
import re
from bs4 import BeautifulSoup
import urllib 
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ParseBrief(object):
    def __init__(self, site):
        self.site = site

        logging.basicConfig(level=logging.DEBUG,\
        format='LOG : %(asctime)s %(message)s',\
        datefmt='%a, %d %b %Y %H:%M:%S', filename = 'log/%s.log' % self.site,\
        filemode = 'w')

    def get_brief(self, tag):
        """
        ps = tag.find_all('p', recursive = False)
        res = ''
        for p in ps:
            res += (p.text + ' ')
        """
        res = tag.text
        return re.sub(r'\n|\t|\r', ' ', res)

    def normal(self, s):
        return re.sub(r'\t|\n|\r', ' ', s)
        
    def parse_nest(self, tag):
        res = ''
        for s in tag.strings:
            res += s
        return res
    
    def request2_(self, url, timeout = 70):
        try:
            res = urllib2.urlopen(url, timeout=timeout)
        except:
            for i in range(10):
                try:
                    res = urllib2.urlopen(url, timeout=timeout)
                except:
                    continue
                else:
                    return res
            return ''
        else:
            return res

    def request_(self, url , timeout=70):
        request = urllib2.Request(url)
        request.add_header('cookie', 'I2KBRCK=1')
        try:
            res = urllib2.urlopen(request, timeout=timeout)
        except:
                for i in range(10):
                    time.sleep(10)
                    try:
                        res = urllib2.urlopen(request, timeout = timeout)
                    except:
                        continue 
                    else:
                        return res
                return ''
        else:
            return res
    def parse_one(self, url):
        pass 

    def parse(self):
        r = open(self.site + '/journal_url', 'r')
        w = open(self.site + '/brief', 'w')
        self.re_catch = open(self.site + '/re_catch', 'w')
        try:
            for line in r:
                if line.strip() == '':
                    continue
                lst = line.split('\t')
                if len(lst) == 1:
                        self.re_catch.write(lst[0] + '\n')
                        continue
                journal = lst[0].strip()
                url = lst[1].strip()
                logging.debug('parsing---- %s' % url)
                self.jour = journal
                self.link = url
                s = self.parse_one(url)
                if s == '':
                    logging.debug('%s?????%s : brief empty!!' % ( journal, url ))
                    self.re_catch.write(url + '\n')
                    continue
                w.write(s)
                logging.debug('catched brief: %s' % s)
                logging.debug('%s finish+++++' % url)
            logging.debug('work finish O(∩_∩)O')
        finally:
            r.close()
            w.close()
