import sys
import pickle

class Site(object):
    def __init__(self, site ):
        this.site = site
        this.path = '/home/disk1/ps/se/scholar-journal/en/luyao/%s/article' % site

    def _get_journal_url(self):
        obj = pickle.load(path)
        home_list = obj.home_list
        f = open(site + '/journal_url', 'w')
        try:
            for url, name in self._journal_url_g():
                f.write(name + '\t' + url + '\n')
        finally:
            f.close()

    def _journal_url_g(self):
        raise Exception('Not implemented!')

