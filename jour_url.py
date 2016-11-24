import pickle

homes = [
        '/home/disk1/ps/se/scholar-journal/en/luyao/tandfonline/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/wiley/issue',
        '/home/disk1/ps/se/scholar-journal/en/luyao/springer/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/cambridge/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/oxford/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/degruyter/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/johns/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/emerald/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/brill/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/chicago/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/duke/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/mit/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/edinburgh/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/california/home',
        '/home/disk1/ps/se/scholar-journal/en/luyao/annual/home'
        ]

for home in homes:
    site = home.split('/')[-2]
    print 'working %s' % site
    obj = pickle.load(open(home))
    home_list = obj.home_list
    f = open(site + '/journal_url', 'w')
    for data1 in home_list:
        for home_url, name in data1[1]:
            f.write(name + '\t' + home_url + '\n')
    f.close()
    print '%s finish!' % site
