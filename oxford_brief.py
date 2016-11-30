# -*- coding: utf-8 -*-
import ParseBrief
import re
from bs4 import BeautifulSoup
import logging
import urlparse
import urllib2
import urllib
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf8')

class Oxford(ParseBrief.ParseBrief):
    def __init__(self, site):
        super(Oxford, self).__init__(site)

    def parse_one3(self, url):
        res = ''
        re2 = self.request_(url)
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')
        res += (self.link.strip() + '\t')
        img = soup.find('img', {'id': 'issueFallbackImage'})
        img_url = ''
        if img:
            img_url = img['src']
        res += (img_url + '\t')
        issn = ''
        issn_div = soup.find('div', {'class': 'journal-footer-colophon'})
        if issn_div:
            ul = issn_div.ul
            p_issn = ''
            e_issn = ''
            for s in ul.strings:
                p = re.search(r'Online ISSN\s*(\w{4,4}\s*-\s*\w{4,4})', s )
                e = re.search(r'Print ISSN\s*(\w{4,4}\s*-\s*\w{4,4})', s)
                if p:
                    p_issn = p.group(1)
                if e:
                    e_issn = e.group(1)
            if p_issn:
                issn = p_issn
            else:
                issn = e_issn
        res += (issn + '\t')
        brief_url_div = soup.find('div', {'class', 'widget widget-SelfServeContent widget-instance-adaptation_Home_Row1_Middle'})
        brief_url = ''
        if brief_url_div:
            if brief_url_div.a:
                brief_url = brief_url_div.a['href']
        r = self.request_(brief_url)
        soup2 = BeautifulSoup(r, 'lxml')
        brief_div = soup2.find('div', {'class':'widget widget-SelfServeContent widget-instance-OupSelfServePage'})
        brief = ''
        if brief_div:
            """
            p = brief_div.p
            brief = self.normal(self.parse_nest(p))
            while not brief.strip() and p:
                p = p.find_next('p')
                if p:
                    brief = self.normal(self.parse_nest(p))
            """
            brief = self.get_brief(brief_div)
        res += (self.normal(brief) + '\n')
        return res

    def parse_one2(self, url):
        res = ''
        brief_url = url.rstrip('/') + '/about'
        re2 = self.request2_(brief_url, 70)
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')
        res += (self.link.strip() + '\t')
        img_div = soup.find('div', {'class': 'cover-issue-image'})
        img_url = ''
        if img_div:
            img_tag = img_div.img
            img_url = img_tag['src']
        else :
            return self.parse_one3(url)
        res += (img_url + '\t')
        issn = ''
        issn_div = soup.find('div', {'id': 'oup-footer-print-issn'})
        if issn_div:
            issn = issn_div.div.string.strip()
        else:
            issn_div = soup.find('div', {'id' : 'oup-footer-online-issn'})
            if issn_div:
                issn = issn_div.div.string.strip()
        res += (issn + '\t')
#        pdb.set_trace()
        brief_div = soup.find('div', {'id': 'oup-about-page-prefix'})
        if not brief_div:
            brief_div = soup.find('div', {'id': 'oup-about-page-suffix'})
            if not brief_div:
                brief_div = soup.find('div', {'class': 'field-item even'})
        brief = ''
        if brief_div:
            """
            p = brief_div.p
            brief = self.normal(self.parse_nest(p))
            while not brief.strip() and p:
                p = p.find_next('p')
                if p:
                    brief = self.normal(self.parse_nest(p))
            """
            brief = self.get_brief(brief_div)
        res += (self.normal(brief) + '\n')
        return res

    def parse_one(self, url):
        res = ''
        re2 = self.request2_(url, 300)
        soup = BeautifulSoup(re2, "lxml")
        res += (self.jour.strip() + '\t')   
        res += (self.link.strip() + '\t')
        img_div_tag = soup.find('div', {'id':'first'})
        if img_div_tag is None:
            return self.parse_one2(url)
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
            try:
                 m = re.search(r'Print ISSN\s*(\w{4,4}\s*-\s*\w{4,4})', issn_tag.string, re.I)
                 if m is not None:
                     issn = m.group(1)
                 else:
                     m = re.search(r'Online ISSN\s*(\w{4,4}\s*-\s*\w{4,4})', issn_tag.string, re.I)
                     if m:
                        issn = m.group(1)
            except TypeError:
                pass
        res += (issn.strip() + '\t')
        m = re.search(r'//(.+?)\.', url)
        journal_name = ''
        if m:
            journal_name = m.group(1)
        brief_url_div = soup.find('div', {'id' : 'second'})
#        ul = brief_url_div.find('ul', {'class' : 'emphasised'})
        brief_url_tag = brief_url_div.li
        if brief_url_tag:
            a = brief_url_tag.a
            if a:
                brief_url = a['href']
        brief = ''
        rr = self.request_(brief_url)
        soup2 = BeautifulSoup(rr, 'lxml')
        brief_div = soup2.find('div', {'id': 'first'})
        if brief_div:
            """
            p = brief_div.p
            brief = self.normal(self.parse_nest(p))
            while not brief.strip() and p:
                p = p.find_next('p')
                if p:
                    brief = self.normal(self.parse_nest(p))
            """
            brief = self.get_brief(brief_div)
        res += (brief.strip() + '\n')
        return res

if __name__ == '__main__':
    b = Oxford('oxford')
    b.parse()
