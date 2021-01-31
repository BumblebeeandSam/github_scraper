import requests
import sys
import random
from time import sleep
from bs4 import BeautifulSoup


def main():
    # Primary script: go to these 7 pages and download the pdfs from them
    for i in range(14,21):
        # Urls of interest are formatted as below
        engine = ScraperPage("https://www.supremecourt.gov/opinions/slipopinion/{}#list".format(i))
        # Find all child urls on page of interest
        engine.discover_all_urls()
        # Go to those urls and download all the pdfs
        engine.download_all_pdfs()
    return 0


class ScraperPage:
    """
    This class  is used for top_level urls that need to be analyzed for
    urls with downloadable content
    """
    def __init__(self, top_url: str):
        """
        url: url is a string that points to the url of the top level
             page being scraped. For the Supreme Court opinions, this
             should be the page for opinions with the 'list' anchor.
             Ex. url = 'https://www.supremecourt.gov/opinions/slipopinion/19#list'
        """
        self.base_url = 'https://www.supremecourt.gov'
        self.top_url = top_url
        self.child_urls = []
        return None

    def discover_all_urls(self):
        data = requests.get(self.top_url).text
        soup = BeautifulSoup(data, "html.parser")
        urls = []
        descs = []
        for ref in soup.find_all('a'):
            if ".pdf" in str(ref):
                try:
                    url = self.base_url + ref['href']
                    desc = ref['title']
                    urls.append(Page(url, desc))
                except:
                    None
        self.child_urls = urls
        self.descs = descs
        return None
    
    def download_all_pdfs(self):
        for page in self.child_urls:
            page.dl_pdf()
        return 0

    
class Page:
    """
    This class is reserved for urls that point to content that we want to d/l
    i.e. urls that point to pdfs
    """
    
    def __init__(self, url: str, desc: str):
        """
        init function to set up the page class
        url: the url that we will download from
        desc: the hovertext when hovering on_top of url from parent page
        """
        self.url = url
        self.desc = desc
        self.filename = url.split('/')[-1]
        return None
    
    def dl_pdf(self):
        sleep(random.randint(5, 10))
        """
        url: string that points to originating url
        filename: a filename for the pdf being d/led.
        Ex. dl_pdf('my_website.com/cool.pdf', 'mypdfdl.pdf')
        saves the file located at 'my_website.com/cool.pdf'
        as a local file called 'mypdfdl.pdf'.
        """
        try:
            with open(self.filename, "wb") as fp:
                data = requests.get(self.url)
                if str(data) == '<Response [200]>':
                    content = data.content
                    fp.write(content)
                else:
                    print(data)
                    print('Error?')
                return 0
        except OSError:
            print("Failed to dl {0}. Can you connect to {0}?".format(self.url))
        except:
            return 1

if __name__ == "__main__":
    sys.exit(main())
