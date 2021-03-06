# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:08:31 2016

@author: v_mahuanhuan
"""

import urllib2
import urlparse
import re
from bs4 import BeautifulSoup
import urllib 

def request_(url , timeout=70):
    res = ''
    try:
        request = urllib2.Request(url)
        request.add_header('cookie', 'I2KBRCK=1')
        res = urllib2.urlopen(request, timeout=timeout)
    except:
        print 'bad request %s!!!' % url
    return res

def parse_brief_url(url):
    re2 = request_(url, 70)
    if re2 == '':
        return ''
    soup = BeautifulSoup(re2, "lxml")
    about = soup.find('div', {'id':'sidebar-global-nav'})
    li = about.find('li', {'class':'first'})
    return li.a['href']
    
def parse_one(url):
    res = ''
    re2 = request_(url, 70)
    if re2 == '':
        return ''
    soup = BeautifulSoup(re2, "lxml")
    title_tag = soup.find('div', {'id':'p7tpc1_1'})
    if title_tag is None:
        return ''
#    assert title_tag, '%s has no title!!!' % url
    title_ul = title_tag.find('ul', {'class':'tablistA'})
    res += (title_ul.li.h2.text.encode('utf8').strip() + '\t')   
    res += (url.strip() + '\t')
    m = re.match( r'(.*?[^/])/[^/].*',url)
    url_prefix = m.group(1)
    img_div_tag = soup.find('ul', {'class':'prodimage'})
    img_url = ''
    img_tag = img_div_tag.img.next_element
    if img_tag is not None:
        img_src = img_tag['src']
        img_url = url_prefix + img_src
    print img_url
    res += (img_url.strip() + '\t')
    issn_div = soup.find('div', {'id': 'p7tpc1_1'})
    issn = ''
    if issn_div is not None:
        issn_dl =issn_div.dl
        for child in issn_dl.children:
            m = re.search(r'ISSN:</b>\s*([\d\w\W]*-[\d\w\W]*?)<', str(child))
            if m is not None:
                print m.group(1)
                issn = m.group(1)
                break
    res += (issn.strip() + '\t')
    
    brief_div = soup.find('div', {'id': 'descript'})
    brief_div2 = brief_div.div.div
#    ps = brief_div2.findAll('p')
    brief = ''
    for s in brief_div2.strings:
        brief += (s.encode('utf8').strip() + ' ')
    brief = normal(brief)
    print 'brief:', brief, '\n'
    res += (brief.strip() + '\n')
    return res

def normal(s):
    res = re.sub(r'<.*?>', '',s)
    res = re.sub(r'\n', ' ',res)
    return res
    
if __name__ == '__main__':
    with open('duke_urls.txt') as r, open('duke.txt', 'w') as w:
        for line in r:
            line = line.strip()
            line = parse_brief_url(line)
            print line
            if not line:
                continue
            s = parse_one(line)
            if s!='':
                w.write(s)
        
    
    
    
    
    
    
    
    