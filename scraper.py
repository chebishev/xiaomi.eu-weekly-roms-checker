from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
load_dotenv()


def get_random_user_agent():
    response = requests.get(
        url='https://headers.scrapeops.io/v1/user-agents',
        params={
            'api_key': os.getenv('SCRAPEOPS_API_KEY'),
            'num_results': '1'}
    )

    return response.json()["result"][0]


def scrape_config_by_url(url):
    page = requests.get(url, headers={'User-Agent': get_random_user_agent()})

    # BeautifulSoup instance that gets url and parser as arguments
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
