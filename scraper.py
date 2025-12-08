from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

session = requests.Session()
cache = {}

def scrape(url):
    if url in cache:
        return cache[url]

    r = session.get(url, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")

    cache[url] = soup
    return soup