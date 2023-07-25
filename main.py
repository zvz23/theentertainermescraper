import os
import re
import json
import parsel
import requests
from db import WebScraperDB
from pprint import pprint



USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
DB_NAME = 'theentertainerme.db'
CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')
URL_REGEX = re.compile(r'\"url\":\"(?P<url>.+)\"')



def parse_company(html: str):
    selector = parsel.Selector(text=html)
    return selector.xpath("//script[@type='application/ld+json']/text()").get()

def scrape_infos():
    urls = []
    with WebScraperDB(DB_NAME) as conn:
        urls = conn.get_all_without_info()
    with requests.Session() as s:
        s.headers.update({'User-Agent': USER_AGENT})
        for url in urls:
            print(url['URL'])
            response = requests.get(url['URL'])
            if response.status_code != 200:
                print("ERROR ", url['URL'])
                continue
            company_info = parse_company(response.text)
            if company_info is not None:
                with WebScraperDB(DB_NAME) as conn:
                    conn.set_info(url['ID'], company_info.strip())
            else:
                print("NO JSON ", url['URL'])
            

if __name__ == '__main__':
    scrape_infos()