
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
import requests
reload(sys)
sys.setdefaultencoding('utf8')

class Mit(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Mit, self).__init__(site)

    def request2_(self, url, timeout=100):
        f=open('/dev/null','w')
        old=sys.stderr
        sys.stderr=f
        request = urllib2.Request(url)
        res=requests.get(url,verify=False,timeout=100)
        sys.stderr=old
        f.close() 
        return res
#    def request2_(self, url, timeout = 100):
#        request = urllib2.Request(url)
#        res=requests.get(url,verify=False,timeout=100)
#        return res

    def parse_one(self, url):
        res = ''
        re2 = self.request2_(url, 300)
        soup = BeautifulSoup(re2.content.decode('utf-8','ignore'), "lxml")
        res += (self.jour.strip() + '\t')   
        res += (self.link.strip() + '\t')
        img_div_tag = soup.find('div', {'class':'cover_image'})
        img_url = ''
        if img_div_tag is not None:
            img = img_div_tag.img
            if img:
                img_src = img['src']
                img_url = urlparse.urljoin(self.link, img_src)
        res += (img_url.strip() + '\t')
        issn = ''
        if img_div_tag:
            issn_tag = img_div_tag.find_next('div')
            if issn_tag:
                m = re.search(r'ISSN:?\s*(\w{4,4}\s*-\s*\w{4,4})', issn_tag.text)
                if m:
                    issn = m.group(1)
                else:
                    m = re.search(r'E-ISSN:?\s*(\w{4,4}\s*-\s*\w{4,4})', issn_tag.text)
                    if m:
                        issn = m.group(1)
        res += (issn.strip() + '\t')
        brief = ''
        brief_div = soup.find('div', {'class': 'aboutJournal'})
        if brief_div:
            brief = self.get_brief(brief_div)
        res += (brief.strip() + '\n')
        return res
if __name__ == '__main__':
    b = Mit('mit')
    b.parse()
