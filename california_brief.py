
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
reload(sys)
sys.setdefaultencoding('utf8')

class California(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(California, self).__init__(site)


    def parse_one(self, url):
        res = ''
        re2 = self.request2_(url, 300)
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')   
        res += (self.link.strip() + '\t')
        img_div_tag = soup.find('div', {'class':'cover-issue-image'})
        img_url = ''
        if img_div_tag is not None:
            img = img_div_tag.img
            if img:
                img_src = img['src']
                img_url = img_src
        res += (img_url.strip() + '\t')
        issn = ''
        issn_tag = soup.find('div', {'id' : 'jnl-ucptemplate-home-cur-iss-snip'})
        if issn_tag:                        
            m = re.search(r'ISSN:.*?(\w{4,4}\s*-\s*\w{4,4})', issn_tag.text)
            if m:
                issn = m.group(1)
            else:
                m = re.search(r'eISSN:.*?(\w{4,4}\s*-\s*\w{4,4})', issn_tag.text)
                if m:
                    issn = m.group(1)
        res += (issn.strip() + '\t')
        brief = ''
        brief_div = soup.find('div', {'id': 'jnl-ucptemplate-about-journal-snippet'})
        if brief_div:
            brief = self.get_brief(brief_div)
        else:
            brief_div = soup.find('div', {'id' : 'jnl-ucptemplate-home-ad1'})
            if brief_div:                         
                brief = self.normal(brief_div.text)

        res += (brief.strip() + '\n')
        return res
if __name__ == '__main__':
    b = California('california')
    b.parse()
