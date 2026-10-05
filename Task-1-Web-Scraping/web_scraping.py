"""
CodeAlpha Task 1 - Web Scraping
Target: Books to Scrape (public demo website)
Run: pip install requests beautifulsoup4 pandas
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CodeAlphaEducationalProject/1.0)"}

def scrape_books(max_pages=3):
    rows = []
    url = BASE_URL
    for _ in range(max_pages):
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for card in soup.select("article.product_pod"):
            title_tag = card.select_one("h3 a")
            price_tag = card.select_one(".price_color")
            rating_tag = card.select_one("p.star-rating")
            rows.append({
                "title": title_tag.get("title", "").strip() if title_tag else "",
                "price": price_tag.get_text(strip=True) if price_tag else "",
                "rating": rating_tag.get("class", ["", ""])[1] if rating_tag and len(rating_tag.get("class", [])) > 1 else "",
                "product_url": BASE_URL + title_tag["href"].replace("../", "") if title_tag else ""
            })

        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        url = BASE_URL + next_link["href"]

    return pd.DataFrame(rows)

if __name__ == "__main__":
    data = scrape_books(max_pages=3)
    data.to_csv("scraped_books.csv", index=False)
    print(f"Saved {len(data)} records to scraped_books.csv")
