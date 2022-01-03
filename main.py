import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import pandas as pd
#Init the colorma module
from pymongo import MongoClient

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

#initialize the set of links
internal_urls = set()
external_urls = set()
link_df = pd.DataFrame()
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    for a_tag in soup.findAll('a'):
        href = a_tag.attrs.get('href')
        if href == "" or href is None:
            continue
        href = urljoin(url,href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + '://' + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    links = pd.Series(list(internal_urls))
    link_df[domain_name] = links
    return urls
#link_df = interlink를 저장한 dataframe

total_urls_visited = 0
def crawl(url, max_urls=30):

    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls = max_urls)



if __name__ == '__main__':
    with open('crawled_urls.txt', 'r') as fd:
        urls = fd.read().splitlines()
        links = pd.DataFrame()
        for u in urls:
            crawl(u)
            print('[+] Total Internal links: ', len(internal_urls))
            print('[+] Total External links: ', len(external_urls))
            print('[+] Total URLs: ', len(external_urls) + len(internal_urls))
        link_df.to_csv('links.csv')
        # Upload database to MongoDB
        # Connect to MongoDB
        # id: 2rhgywls
        # pw: ynkie_0110
        client = MongoClient(
          "mongodb+srv://2rhgywls:ynkie_0110@cluster1.mpacz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        # database name: target
        # collection name: collection_link
        db = client['target']
        collection = db['collection_link']

        link_df.reset_index(inplace=True)
        df_dict = link_df.to_dict('records')
        collection.insert_many(df_dict)


