import re
import requests
from bs4 import BeautifulSoup

pages = set()


def get_links(page_url):
    global pages
    pattern = re.compile("^(/)")
    html = requests.get(f"your_URL{page_url}").text  # fstrings require Python 3.6+
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a", href=pattern):
        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                new_page = link.attrs["href"]
                print(new_page)
                pages.add(new_page)
                get_links(new_page)


with open('crawled_urls.txt','r') as fd:
    urls = fd.read().splitlines()
    for u in urls:
        links = get_links(u)
        df_link[domain] = links
    print(df_link)
    df_link.to_csv('Crawled.csv')
