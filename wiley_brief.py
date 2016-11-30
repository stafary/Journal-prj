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

class Wiley(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Wiley, self).__init__(site)

    def parse_one(self, url):
        res = ''
        url2 = url.rstrip('/') + '/homepage/ProductInformation.html'  
        re2 = self.request2_(url2)
        if not re2:
            re2 = self.request2_(url)
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')   
        res += (self.link.strip() + '\t')
        img_div_tag = soup.find('div', {'class':'imgShadow'})
        img_url = ''
        if img_div_tag is not None:
            img = img_div_tag.img
            if img:
                img_src = img['src']
                img_url = img_src
        res += (img_url.strip() + '\t')
        issn = ''
        m = re.search(r'\(ISSN\)(\w{4,4}\s*-\s*\w{4,4})', url, re.I)
        if m:
            issn = m.group(1)
        res += (issn.strip() + '\t')
        brief = ''
        brief_div = soup.find('div', {'id': 'homepageContent'})
        if brief_div:
            brief = self.normal(brief_div.text)
        res += (brief.strip() + '\n')
        return res

    def normal(self, s):
        return re.sub('\t|\r|\n|\s{2,}', '  ', s)
if __name__ == '__main__':
    b = Wiley('wiley')
    b.parse()
