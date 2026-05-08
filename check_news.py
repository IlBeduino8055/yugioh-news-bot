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

# Prima news
article = soup.select_one("article")

if article is None:
    print("Nessuna news trovata")
    exit()

# Link
link_tag = article.select_one("a")
link = link_tag.get("href")

if link.startswith("/"):
    link = "https://www.yugioh-card.com" + link

# Titolo
title_tag = article.select_one("h2, h3, .title")
title = title_tag.get_text(strip=True) if title_tag else "Nuova News"

# Immagine
img_tag = article.select_one("img")
image = img_tag.get("src") if img_tag else None

if image and image.startswith("/"):
    image = "https://www.yugioh-card.com" + image

LAST_FILE = "last_news.txt"

last_link = ""

if os.path.exists(LAST_FILE):
    with open(LAST_FILE, "r") as f:
        last_link = f.read().strip()

if link != last_link:

    embed = {
        "title": title,
        "url": link,
        "description": "📰 Nuova news dal sito ufficiale Yu-Gi-Oh!",
        "color": 16711680
    }

    # Aggiunge immagine se esiste
    if image:
        embed["image"] = {
            "url": image
        }

    data = {
        "username": "Yu-Gi-Oh News",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=data)

    with open(LAST_FILE, "w") as f:
        f.write(link)

    print("Nuova news inviata!")

else:
    print("Nessuna nuova news")
