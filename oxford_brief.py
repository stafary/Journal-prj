import ParseBrief
import re
from bs4 import BeautifulSoup
import logging
import urlparse
import urllib2
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Oxford(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Oxford, self).__init__(site)

    def parse_one(self, url):
        res = ''
        try:
            re2 = self.request_(url, 100)
        except:
            return ''
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')   
        res += (url.strip() + '\t')
#        m = re.match( r'(.*?[^/])/[^/].*',url)
#        url_prefix = m.group(1)
        img_div_tag = soup.find('div', {'id':'first'})
        if img_div_tag is None:
            return ''
        img_url = ''
        img_tag = img_div_tag.img
        if img_tag is not None:
            img_src = img_tag['src']
            url_prefix = url.strip('/')
            img_url = url_prefix + img_src
        res += (img_url.strip() + '\t')
        issn_tag = soup.find('div', {'id': 'issn'})
        issn = ''
        if issn_tag is not None:
            m = re.search(r'Print ISSN\s*(\d+-\d+)', issn_tag.string, re.I)
            if m is not None:
                issn = m.group(1)
            else:
                m = re.search(r'Online ISSN\s*(\d+-\d+)', issn_tag.string, re.I)
                issn = m.group(1)
        res += (issn.strip() + '\t')
        brief_div = soup.find('div', {'class': 'section'})
        brief = ''
        if brief_div is not None and brief_div.p is not None:
            p = brief_div.p
            for child in p.children:
               name = child.name
               if name is not None and name == 'em':
                    brief += child.string.encode('utf8')
                    brief += re.sub(r'\s{2,}|\t|\n', '', child.next_sibling)
        res += (brief.strip() + '\n')
        return res

if __name__ == '__main__':
    b = Oxford('oxford')
    b.parse()
