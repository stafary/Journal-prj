
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
reload(sys)
sys.setdefaultencoding('utf8')

class Emerald(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Emerald, self).__init__(site)


    def parse_one(self, url):
        res = ''
        re2 = self.request_(url, 300)
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')   
        res += (self.link.strip() + '\t')
        img_div_tag = soup.find('div', {'class':'jnlHeadBox'})
        img_url = ''
        if img_div_tag is not None:
            img = img_div_tag.img
            if img:
                img_src = img['src']
                img_url = urlparse.urljoin(self.link, img_src)
        res += (img_url.strip() + '\t')
        issn = ''
        if img_div_tag:
            m = re.search(r'ISSN:?\s*(\w{4,4}\s*-\s*\w{4,4})', img_div_tag.text, re.I)
            if m:
                issn = m.group(1)
        res += (issn.strip() + '\t')
        brief = ''
        if img_div_tag:
            h = img_div_tag.find_next('h3', text = re.compile(r'scope|Scope|cover|Cover'))
            if h:
                sib = h.next_sibling
                while sib:
                    if type(sib) != bs4.element.NavigableString:
                        if type(sib) == bs4.element.Comment:
                            continue
                        if sib.name == 'h3':
                            break
                        else:
                            brief += sib.text
                    else:
                        brief += str(sib)
                    sib = sib.next_sibling
            else:
               div2 = img_div_tag.next_sibling
               while div2 and not brief.strip():
                 while type(div2) != bs4.element.Tag:
                     div2 = div2.next_sibling
                 try:
                      brief = div2.text
                 except:
                      brief = div2.string
                 div2 = div2.next_sibling
        brief = re.sub(r'\t|\n|\r', ' ', brief)
        res += (brief.strip() + '\n')
        return res
if __name__ == '__main__':
    b = Emerald('emerald')
    b.parse()
