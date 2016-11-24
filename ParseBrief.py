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

    def request_(self, url , timeout=70):
        request = urllib2.Request(url)
        request.add_header('cookie', 'I2KBRCK=1')
        res = urllib2.urlopen(request, timeout=timeout)
        if not res:
            for i in range(10):
                time.sleep(10)
                res = urllib2.urlopen(request, timeout = timeout)
                if res:
                    return res
        return None
        
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
                try:
                    self.jour = journal
                    s = self.parse_one(url)
                except Exception as e:
                    logging.error('url: %s WA ****check your func parse_one' % url)
                    logging.error(repr(e))
                    raise e
                if s == '':
                    logging.debug('%s?????%s : brief empty!!' % ( journal, url ))
                    self.re_catch.write(url + '\n')
                    continue
                w.write(s)
                logging.debug('%s finish+++++' % url)
            logging.debug('work finish O(∩_∩)O')
        finally:
            r.close()
            w.close()
