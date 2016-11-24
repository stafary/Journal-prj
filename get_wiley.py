import sys
import get_url

class Wiley(get_url.Site):

    def __init__(self, site):
        super(Wiley, self).__init__(site)
        self.path = '/home/disk1/ps/se/scholar-journal/en/luyao/%s/issue' % self.site
    def _journal_url_g(self):
        for data1 in self.home_list:
            index_url = data1[0]
            for home_url, name in data1[1]:
                yield home_url + '/issues', name

if __name__ == '__main__':
    t = Wiley('wiley')
    t._get_journal_url()
