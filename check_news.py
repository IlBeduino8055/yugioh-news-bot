import requests
from bs4 import BeautifulSoup
import os
import json

WEBHOOK_URL = os.environ['WEBHOOK_URL']

URL = "https://www.yugioh-card.com/en/news/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

article = soup.find("a")

title = article.text.strip()
link = article.get("href")

if not link.startswith("http"):
    link = "https://www.yugioh-card.com" + link

last_news_file = "last_news.txt"

last_news = ""

if os.path.exists(last_news_file):
    with open(last_news_file, "r") as f:
        last_news = f.read().strip()

if link != last_news:

    data = {
        "username": "Yu-Gi-Oh News",
        "embeds": [{
            "title": title,
            "description": "Nuova news trovata!",
            "url": link,
            "color": 16711680
        }]
    }

    requests.post(WEBHOOK_URL, json=data)

    with open(last_news_file, "w") as f:
        f.write(link)
