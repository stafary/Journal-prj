# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:08:31 2016

@author: v_mahuanhuan
"""

import urllib2
import urlparse
import re
from bs4 import BeautifulSoup
import bs4
import urllib 

def request_(url , timeout=70):
    request = urllib2.Request(url)
    request.add_header('cookie', 'I2KBRCK=1')
    res = urllib2.urlopen(request, timeout=timeout)
    return res

res2 = request_('http://www.journals.uchicago.edu/journals/aft/about', 100)
soup = BeautifulSoup(res2, 'lxml')
div = soup.find('div', {'id':'rich-text-218e8c77-a808-45c1-9df4-1601c0fcbe49'})

p = div.p
p = p.next_sibling
if not p.string.strip():
    p = p.next_sibling
for a in p.strings:
    print a

#brief_div = soup.find('div', {'class': 'section'})
#print brief_div.p
#for a in brief_div.p.children:
#    
#    if a.name == 'em':
#        print re.sub(r'\s{2,}|\t|\n', '', a.next_sibling)
#    print type(a) is 'bs4.element.NavigableString'