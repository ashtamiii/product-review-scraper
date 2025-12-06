import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_snapdeal_product(url: str, max_pages: int = 3):
    all_reviews = []

    print(f"Fetching URL: {url}")

    for page in range(1, max_pages + 1):
        paged_url = f"{url}?page={page}"
        print(f"Trying page {page}: {paged_url}")

        resp = requests.get(paged_url, headers=HEADERS, timeout=15)

        print("Status code:", resp.status_code)

        if resp.status_code != 200:
            print(f"Page {page} failed with status {resp.status_code}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        # This selector works on many Snapdeal layouts
        blocks = soup.select("div.user-review") or soup.select("div.commentlist")

        if not blocks:
            print(f"No reviews found on page {page}. Stopping.")
            break

        for block in blocks:
            title_tag = block.find("div", class_="head")
            body_tag = block.find("p")
            rating_tag = block.find("span", class_="rating")

            title = title_tag.text.strip() if title_tag else ""
            body = body_tag.text.strip() if body_tag else ""
            rating = None

            if rating_tag:
                try:
                    rating = float(rating_tag.text.strip())
                except:
                    rating = None

            all_reviews.append({
                "platform": "snapdeal",
                "product_url": url,
                "title": title,
                "body": body,
                "rating": rating
            })

        time.sleep(1)

    df = pd.DataFrame(all_reviews)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/snapdeal_reviews.csv", index=False)

    print(f"Saved {len(all_reviews)} reviews to data/snapdeal_reviews.csv")

    return all_reviews
