
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

class Edinburgh(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Edinburgh, self).__init__(site)


    def parse_one(self, url):
        res = ''
        re2 = self.request_(url, 300)
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')   
        res += (self.link.strip() + '\t')
        img_div_tag = soup.find('div', {'class':'publicationCoverImage'})
        img_url = ''
        if img_div_tag is not None:
            img = img_div_tag.img
            if img:
                img_src = img['src']
                img_url = urlparse.urljoin(self.link, img_src)
        res += (img_url.strip() + '\t')
        issn = ''
        issn_tag = soup.find('span', {'class' : 'serial-item serialDetailsIssn'})
        if issn_tag:
            m = re.search(r'(\w{4,4}\s*-\s*\w{4,4})', issn_tag.text)
            if m:
                issn = m.group(1)
        else:
            issn_tag = soup.find('span', {'class' : 'serial-item serialDetailsEissn'})
            if issn_tag:
                m = re.search(r'(\w{4,4}\s*-\s*\w{4,4})', issn_tag.text)
                if m:
                    issn = m.group(1)
        res += (issn.strip() + '\t')
        brief = ''
        brief_div = soup.find('div', {'id': 'rich-text-2dbeaa87-e34f-474a-96be-10ad3b8cfa3d'})
        if brief_div:
            brief = self.get_brief(brief_div)
        res += (brief.strip() + '\n')
        return res
if __name__ == '__main__':
    b = Edinburgh('edinburgh')
    b.parse()
