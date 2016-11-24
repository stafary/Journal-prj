import sys
import urlparse
import get_url

class Springer(get_url.Site):

    def __init__(self, site):
        super(Springer, self).__init__(site)

    def _journal_url_g(self):
        postfix='/content/by/year'
        for data1 in self.home_list:
            index_url = data1[0]
            for home_url, name in data1[1]:
                link = urlparse.urljoin(home_url, postfix)
                yield link, name

if __name__ == '__main__':
    t = Springer('springer')
    t._get_journal_url()
