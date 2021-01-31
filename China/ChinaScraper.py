import requests
import sys
import random
from time import sleep
from bs4 import BeautifulSoup


def main():
    # Primary script: go to China's government page + 1 layer down from their main page
    # Discover all images, then download them

    # Base url for the webpage
    start_url = 'http://www.gov.cn'
    # Starting off the start_url = current_url, will differ later
    current_url = start_url
    # Create the engine to d/l stuff
    engine = ScraperPage(start_url, current_url)
    # Find all child urls & image urls on page of interest
    engine.discover()
    # Go to those urls and download all the images
    engine.download_all_images()
    for url in engine.child_urls:
        # same as above, except 1 layer down from main page
        # Could be recursive but not set-up for that as it's a Sunday project - would
        # have to ensure that we do not see pages from before to avoid looping
        engine1 = ScraperPage(start_url, current_url)
        sleep(random.randint(5,10))
        engine1.discover()
        engine1.download_all_images()
    return 0


class ScraperPage:
    """
    This class  is used for top_level urls that need to be analyzed for
    urls with downloadable content
    """
    def __init__(self, base_url: str, current_url: str):
        """
        url: url is a string that points to the url of the top level
             page being scraped. 
        """
        self.data = requests.get(current_url).text
        self.base_url = base_url
        self.child_urls = []
        self.img_urls = []
        self.pdf_urls = []
        return None

    def discover(self):
        # Function to call all the discover functions at once
        self.discover_all_pictures()
        self.discover_all_urls()
        return None

    def discover_all_pictures(self):
        # Find all the image urls on the page
        soup = BeautifulSoup(self.data, "html.parser")
        urls = []
        # descs = []
        for ref in soup.find_all('img'):
            img_url = ref['src']
            if self.base_url not in img_url:
                if 'http' not in img_url:
                    img_url = self.base_url + img_url
                    urls.append(img_url)
            else:
                 urls.append(img_url)   
        self.img_urls = [Page(url) for url in urls]
        # self.descs = descs
        return None
    
    def discover_all_urls(self):
        soup = BeautifulSoup(self.data, "html.parser")
        urls = []
        # descs = []
        for ref in soup.find_all('a'):
            # print(ref)
            try:
                new_page_url = ref['href']
                if 'http' in new_page_url:
                    if 'gov.cn' in new_page_url:
                        urls.append(new_page_url)
                    else:
                        None
                else:
                    if 'javascript' in new_page_url:
                        None
                    else:
                        new_page_url = self.base_url + new_page_url
                        urls.append(url)
            except:
                None
        self.child_urls = urls
        # self.descs = descs
        return None
    
    def download_all_images(self):
        for image in self.img_urls:
            image.dl()
        return 0

    
class Page:
    """
    This class is reserved for urls that point to content that we want to d/l
    i.e. urls that point to pdfs
    """
    
    def __init__(self, url: str):
        """
        init function to set up the page class
        url: the url that we will download from
        desc: the hovertext when hovering on_top of url from parent page
        """
        self.url = url
        self.filename = url.split('/')[-1]
        return None
    
    def dl(self):
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
