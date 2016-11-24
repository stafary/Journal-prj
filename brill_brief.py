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

class Brill(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Brill, self).__init__(site)

    def parse_one(self, url):
        res = ''
        try:
            re2 = self.request_(url, 70)
        except:
            return ''
        soup = BeautifulSoup(re2, "lxml")
        title_tag = soup.find('div', {'id':'itemTitle'})
        if title_tag is None:
            return ''
        res += (title_tag.h1.text.encode('utf8').strip() + '\t')   
        res += (url.strip() + '\t')
        m = re.match( r'(.*?[^/])/[^/].*',url)
        url_prefix = m.group(1)
        img_div_tag = soup.find('div', {'class':'journaltopleft'})
        img_url = ''
        img_tag = img_div_tag.img
        if img_tag is not None:
            img_src = img_tag['src']
            img_url = url_prefix + img_src
        res += (img_url.strip() + '\t')
        issn_tag = soup.find('span', {'class': 'meta-value issn'})
        issn = ''
        if issn_tag is not None:
            issn = issn_tag.text.encode('utf8')
        res += (issn.strip() + '\t')
        brief_div = soup.find('div', {'class': 'journaltopright'})
        brief = ''
        if brief_div is not None:
            brief_p = brief_div.p
            brief = brief_p.text.encode('utf8')
            brief = re.sub(r'<.*?>', '',brief)
            brief = re.sub(r'\n', ' ',brief)
    #        print brief
        res += (brief.strip() + '\n')
        return res

if __name__ == '__main__':
    b = Brill('brill')
    b.parse()
