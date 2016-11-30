# -*- coding: utf-8 -*-
import ParseBrief
import re
from bs4 import BeautifulSoup
import logging
import urlparse
import urllib2
import urllib
import sys
import urlparse
import pdb
import bs4
import requests
reload(sys)
sys.setdefaultencoding('utf8')

class Cambridge(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Cambridge, self).__init__(site)

    def request_(self, url, timeout=100):
        f=open('/dev/null','w')
        old=sys.stderr
        sys.stderr=f
        request = urllib2.Request(url)
        res=requests.get(url,verify=False,timeout=100)
        sys.stderr=old
        f.close() 
        return res

    def parse_one(self, url):
        res = ''
        re2 = ''
        try:
            re2 = self.request_(url, 300)
        except:
            for i in range(10):
                try:
                    re2 = self.request_(url, 300)
                except:
                    continue
                else:
                    break
            return ''
        soup = BeautifulSoup(re2.content.decode('utf-8','ignore'),"lxml")
        res += (self.jour.strip() + '\t')   
        res += (self.link.strip() + '\t')
        img_div_tag = soup.find('div', {'class':'clearfix details-container'})
        img_url = ''
        if img_div_tag is not None:
            img = img_div_tag.img
            if img:
                img_src = img['src']
                img_url = img_src
        res += (img_url.strip() + '\t')
        issn = ''
        if img_div_tag:
            ul = img_div_tag.find('ul', {'class' : 'overview clear-none'})
            m = re.search(r'(\w{4,4}\s*-\s*\w{4,4})\s?\(Print\)', ul.text, re.I)
            if m:
                issn = m.group(1)
            else:
                m = re.search(r'(\w{4,4}\s*-\s*\w{4,4})\s?\(Online\)', ul.text, re.I)
                if m:
                    issn = m.group(1)
        res += (issn.strip() + '\t')
        brief = ''
        if img_div_tag:
            ul = img_div_tag.find('ul', {'class' : 'overview clear-none'})
            if ul:
                brief_div = ul.find_next_sibling('div', {'class' : 'description'})
            if brief_div:
                brief = brief_div.text
                brief = re.sub('\n|\r|\t', ' ', brief).strip()
            if not brief:
                brief_div = soup.find('div', {'id' : '57ebce4d68592c704b7e68d0'})
                if brief_div:
                    brief = brief_div.text
                    brief = re.sub('\n|\r|\t', ' ', brief).strip()
        res += (brief.strip() + '\n')
        return res

if __name__ == '__main__':
    b = Cambridge('cambridge')
    b.parse()
