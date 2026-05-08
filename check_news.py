import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ['WEBHOOK_URL']

URL = "https://www.yugioh-card.com/eu/news/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Cerca la prima news vera
article = soup.select_one("article a")

if article is None:
    print("Nessuna news trovata")
    exit()

title = article.get_text(strip=True)
link = article.get("href")

# Sistema link relativo
if link.startswith("/"):
    link = "https://www.yugioh-card.com" + link

LAST_FILE = "last_news.txt"

last_link = ""

if os.path.exists(LAST_FILE):
    with open(LAST_FILE, "r") as f:
        last_link = f.read().strip()

# Invia solo se nuova
if link != last_link:

    data = {
        "username": "Yu-Gi-Oh News",
        "embeds": [
            {
                "title": title,
                "url": link,
                "description": "📰 Nuova news dal sito ufficiale Yu-Gi-Oh!",
                "color": 16711680
            }
        ]
    }

    requests.post(WEBHOOK_URL, json=data)

    with open(LAST_FILE, "w") as f:
        f.write(link)

    print("Nuova news inviata!")
else:
    print("Nessuna nuova news")
