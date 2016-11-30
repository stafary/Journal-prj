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

class Duke(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Duke, self).__init__(site)

    def parse_brief_url(self, url):
        re2 = self.request_(url, 70)
        ok = False
        if not re2:
            raise Exception('page loss---url:%s' % url)
            return ''
        soup = BeautifulSoup(re2, "lxml")
        about = soup.find('div', {'id':'sidebar-global-nav'})
        li = about.find('li', {'class':'first'})
        return li.a['href']
        
    def parse_one(self, url):
        res = ''
        re2 = self.request_(url, 200)
        soup = BeautifulSoup(re2, "lxml")
        title_tag = soup.find('div', {'id':'p7tpc1_1'})
        if title_tag is None:
            raise Exception('no title~ url: %s' % url)
            return ''
    #    assert title_tag, '%s has no title!!!' % url
        title_ul = title_tag.find('ul', {'class':'tablistA'})
        res += (title_ul.li.h2.text.encode('utf8').strip() + '\t')   
        res += (self.link.strip() + '\t')
        m = re.match( r'(.*?[^/])/[^/].*',url)
        url_prefix = m.group(1)
        img_div_tag = soup.find('ul', {'class':'prodimage'})
        img_url = ''
        img_tag = img_div_tag.img.next_element
        if img_tag is not None:
            img_src = img_tag['src']
            img_url = url_prefix + img_src
        res += (img_url.strip() + '\t')
        issn_div = soup.find('div', {'id': 'p7tpc1_1'})
        issn = ''
        if issn_div is not None:
            issn_dl =issn_div.dl
            for child in issn_dl.children:
                m = re.search(r'ISSN:</b>\s*(\w{4,4}\s*-\s*\w{4,4})<', str(child))
                if m is not None:
                    issn = m.group(1)
                    break
        res += (issn.strip() + '\t')
        
        brief_div = soup.find('div', {'id': 'descript'})
        brief_div2 = brief_div.div.div
    #    ps = brief_div2.findAll('p')
        brief = ''
        for s in brief_div2.strings:
            brief += (s.encode('utf8').strip() + ' ')
        brief = self.normal(brief)
        res += (brief.strip() + '\n')
        return res

    def normal(self, s):
        res = re.sub(r'<.*?>', '',s)
        res = re.sub(r'\n', ' ',res)
        return res

    def parse(self):
        r = open(self.site + '/journal_url', 'r')
        w = open(self.site + '/brief', 'w')
        try:
            for line in r:
                lst = line.split('\t')
                try:
                    journal = lst[0].strip()
                    url = lst[1].strip()
                    self.link = url
                    url = self.parse_brief_url(url)
                    logging.debug('parsing %s' % url)
                    s = self.parse_one(url)
                    if s == '':
                        logging.debug('%s-%s : brief empty!!' % ( journal, url ))
                        continue
                    w.write(s)
                    logging.debug('%s finish!!' % url)
                except Exception as e:
                    logging.error(repr(e))
                    raise e
        finally:
            r.close()
            w.close()
if __name__ == '__main__':
    b = Duke('duke')
    b.parse()
