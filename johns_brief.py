# -*- coding: utf-8 -*-
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

class Johns(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Johns, self).__init__(site)

    def parse_one(self, url):
        res = ''
        re2 = self.request_(url, 70)
        soup = BeautifulSoup(re2, "lxml")
        title_tag = soup.find('div', {'id':'journalsrightcolumn'})
        assert title_tag, 'No title####'
    #    assert title_tag, '%s has no title!!!' % url
        res += (title_tag.h2.text.encode('utf8') + '\t')   
        res += (url + '\t')
        m = re.match( r'(.*?[^/])/[^/].*',url)
        url_prefix = m.group(1)
        img_div_tag = soup.find('div', {'id':'journalsleftcolumn'})
        img_url = ''
        img_tag = img_div_tag.img
        if img_tag is not None:
            img_src = img_tag['src']
            img_url = url_prefix + img_src
        res += (img_url + '\t')
        issn_tag = soup.find('div', {'id': 'journalspecs'})
        issn = ''
        if issn_tag is not None:
            tmp = issn_tag.text.encode('utf8')
            m = re.search(r'Print ISSN:\s*(\w{4,4}\s*-\s*\w{4,4})Online', tmp)
            if m is not None:
                issn = m.group(1)
        res += (issn.strip() + '\t')
        brief_div = soup.find('div', {'id': 'journalsrightcolumn'})
        brief = ''
        if brief_div is not None:
            brief_p = brief_div.p
            brief = brief_p.text.encode('utf8')
        res += (brief.strip() + '\n')
        return res

if __name__ == '__main__':
    b = Johns('johns')
    b.parse()
