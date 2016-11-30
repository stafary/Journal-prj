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

class Chicago(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Chicago, self).__init__(site)

    def parse_brief_url(self, url):
        re2 = self.request_(url, 300)
        soup = BeautifulSoup(re2, "lxml")
        ul = soup.find('ul', {'class':'primaryNav'})
        if ul:
            a = ul.find(href = re.compile(r'journals/.+/about'))
            if not a:
                return ''
            m = re.match( r'(.*?[^/])/[^/].*',url)
            url_prefix = m.group(1)
            return url_prefix + a['href']
        return ''
    def parse_one(self, url):
        re2 = self.request_(url, 70)
        soup = BeautifulSoup(re2, "lxml")
        res = ''
        res += (self.jour + '\t')   
        res += (self.link.strip() + '\t')
        m = re.match( r'(.*?[^/])/[^/].*',url)
        url_prefix = m.group(1)
        img_div_tag = soup.find('div', {'class':'publicationCoverImage'})
        assert img_div_tag, '%s has no Image' % url
        img_url = url_prefix + img_div_tag.img['src']
        res += (img_url.strip() + '\t')
        issn_div = soup.find('div', {'id':'rich-text-218e8c77-a808-45c1-9df4-1601c0fcbe49'})
        issn = ''
        if issn_div:
            child =  issn_div.p.find(text = re.compile(r'(\w{4,4}\s*-\s*\w{4,4})'))
            if child:
                issn = child.strip(' |')
                res += (issn.strip() + '\t')
            else:
                issn = ''
                res += ('\t')
        
    #    ps = brief_div2.findAll('p')
        brief = ''
        p = issn_div.p
        if issn:
            p = p.next_sibling
            if not p.string.strip():
                p = p.next_sibling
        assert p, '%s no abstract' % url
        for s in p.strings:
            brief += s
        res += (brief + '\n')
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
                    journal = lst[0].strip()
                    url = lst[1].strip()
                    self.jour = journal
                    self.link = url
                    url = self.parse_brief_url(url)
                    if url == '':
                        logging.error('journal:%s ~~~~url:%s has no brief url' % (self.jour, url))
                        continue
                    logging.debug('------parsing %s' % url)
                    s = self.parse_one(url)
                    if s == '':
                        logging.debug('%s-%s : brief empty!!' % ( journal, url ))
                        continue
                    w.write(s)
                    logging.debug('++++++%s finish!!' % url)
        finally:
            r.close()
            w.close()
if __name__ == '__main__':
    b = Chicago('chicago')
    b.parse()
