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
    request = urllib2.Request(url)
    request.add_header('cookie', 'I2KBRCK=1')
    res = urllib2.urlopen(request, timeout=timeout)
    return res
    
def parse_one(url):
    res = ''
    try:
        re2 = request_(url, 70)
    except:
        print 'error url: %s' % url
        return ''
    soup = BeautifulSoup(re2, "lxml")
    title_tag = soup.find('div', {'id':'itemTitle'})
    if title_tag is None:
        return ''
#    assert title_tag, '%s has no title!!!' % url
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
    with open('brill_urls.txt') as r, open('brill.txt', 'w') as w:
        for line in r:
            line = line.strip()
            if not line:
                continue
            s = parse_one(line)
            if s!='':
                w.write(s)
        
    
    
    
    
    
    
    
    