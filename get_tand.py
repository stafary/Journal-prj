import sys
import get_url

class Tand(get_url.Site):

    def __init__(self, site):
        super(Tand, self).__init__(site)

    def _journal_url_g(self):
        print len(self.home_list)
        for data1 in self.home_list:
            index_url = data1[0]
            for home_url, name in data1[1]:
                if home_url.endswith('/current'):
                    home_url = home_url[:-len('/current')].replace('/toc/', '/loi/')
                yield home_url, name

if __name__ == '__main__':
    t = Tand('tandfonline')
    t._get_journal_url()
