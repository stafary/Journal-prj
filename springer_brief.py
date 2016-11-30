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

class Springer(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Springer, self).__init__(site)

    def parse_one(self, url):
        res = ''
        re2 = self.request2_(url, 300)
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')   
        res += (self.link.strip() + '\t')
        img_tag = soup.find('img', {'class':'look-inside-cover'})
        img_url = ''
        if img_tag:
            img_url = img_tag['src']
        res += (img_url.strip() + '\t')
        issn = ''
        issn_div = soup.find('div', {'id' : 'issn'})
        if issn_div:
            m = re.search('(\w{4,4}\s*-\s*\w{4,4})\s*?\(Print\)', issn_div.text)
            if m:
                issn = m.group(1)
            else:
                m = re.search('(\w{4,4}\s*-\s*\w{4,4})\s*?\(Online\)', issn_div.text)
                if m:
                    issn = m.group(1)
        res += (issn.strip() + '\t')
        brief = ''
        brief_div = soup.find('div', {'class' : 'abstract-content formatted'})
        if brief_div:
            brief = self.normal(brief_div.text)
        res += (brief.strip() + '\n')
        return res
    def search_p(self, tag):
        ps = tag.find_all('p')
        if ps:
            for p in ps:
                if p.text.strip():
                    return p.text
        else:
            return ''
if __name__ == '__main__':
    b = Springer('springer')
    b.parse()
