from urllib.parse import urljoin
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://books.toscrape.com/"
session = requests.Session()
books_data = []

# بناء خريطة للـ categories من القائمة الجانبية

home_soup = BeautifulSoup(session.get(base_url, timeout=15).text, "html.parser")
category_map= {}
for a in home_soup.select("div.side_categories ul li ul li a"):
  cat_name = a.get_text(strip=True) or "unknown"
  cat_url = urljoin(base_url, a.get("href", ""))
  category_map[cat_url] = cat_name

# لفة على الصفحات (من 1 لـ 50 أو لحد ما تخلص الصفحات)
for page in range(1, 51):
  page_url = (
      base_url
      if page == 1
      else urljoin(base_url, f"catalogue/page-{page}.html")
  )
  resp = session.get(page_url, timeout=15)
  if resp.status_code != 200:
    break

  soup = BeautifulSoup(resp.text, "html.parser")
  articles = soup.select("article.product_pod")
  if not articles:
    break

  for item in articles:
    title_el = item.select_one("h3 a")
    title = (
        (title_el.get("title") or title_el.get_text(strip=True))
        if title_el
        else "unknown"
    ) or "unknown"

    price_el = item.select_one("p.price_color")
    price = (price_el.get_text(strip=True) if price_el else "") or "unknown"

    stock_el = item.select_one("p.instock.availability")
    stock = (stock_el.get_text(" ", strip=True) if stock_el else "") or "unknown"

    book_href = title_el.get("href", "") if title_el else ""
    book_url = urljoin(page_url, book_href) if book_href else ""

    category = "unknown"
    if book_url:
      b_resp = session.get(book_url, timeout=15)
      if b_resp.status_code == 200:
        b_soup = BeautifulSoup(b_resp.text, "html.parser")
        crumbs = b_soup.select("ul.breadcrumb li a")
        if len(crumbs) >= 3:
          category = crumbs[2].get_text(strip=True) or "unknown"

    books_data.append({
        "category": category,
        "title": title,
        "price": price,
        "in_stock": stock,
    })

  time.sleep(0.2)

df = pd.DataFrame(books_data)
df.to_csv("books.csv", index=False, encoding="utf-8-sig")
print("Saved rows:", len(df))