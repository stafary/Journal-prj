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
    re2 = request_(url, 70)
    soup = BeautifulSoup(re2, "lxml")
    title_tag = soup.find('div', {'id':'journalsrightcolumn'})
    if title_tag is None:
        return ''
#    assert title_tag, '%s has no title!!!' % url
    res += (title_tag.h2.text.encode('utf8') + '\t')   
    res += (url + '\t')
    m = re.match( r'(.*?[^/])/[^/].*',url)
    url_prefix = m.group(1)
    img_div_tag = soup.find('div', {'id':'journalsleftcolumn'})
    img_url = ''
    img_tag = img_div_tag.img
    if img_tag is not None:
        print img_tag
        img_src = img_tag['src']
        img_url = url_prefix + img_src
    res += (img_url + '\t')
    issn_tag = soup.find('div', {'id': 'journalspecs'})
    issn = ''
    if issn_tag is not None:
        tmp = issn_tag.text.encode('utf8')
        m = re.search(r'Print ISSN:\s*([\w\W\d]*-[\d\w\W]*?)Online', tmp)
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
    with open('johns_urls.txt') as r, open('johns.txt', 'w') as w:
        for line in r:
            line = line.strip()
            if not line:
                continue
            s = parse_one(line)
            if s!='':
                w.write(s)
        
    
    
    
    
    
    
    
    