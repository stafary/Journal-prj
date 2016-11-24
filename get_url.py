import sys
import pickle

class Site(object):
    def __init__(self, site ):
        self.site = site
        self.path = '/home/disk1/ps/se/scholar-journal/en/luyao/%s/home' % site

    def _get_journal_url(self):
        obj = pickle.load(open(self.path))
        self.home_list = obj.home_list
        print 'father home_list len: %d' % len(self.home_list) 
        f = open(self.site + '/journal_url', 'w')
        try:
            for url, name in self._journal_url_g():
                f.write(name + '\t' + url + '\n')
        finally:
            f.close()

    def _journal_url_g(self):
        raise Exception('Not implemented!')

