import parsel
from db import WebScraperDB

with open('test.html', 'r', encoding='utf-8') as f:
    html = f.read()
    selector = parsel.Selector(html)
    urls = [[url] for url in selector.xpath("//div[@class='row']/div/a/@href").getall()]

    with WebScraperDB('theentertainerme.db') as conn:
        conn.save_urls(urls)
