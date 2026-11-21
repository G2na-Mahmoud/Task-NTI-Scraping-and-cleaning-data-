# Book Scraping Task

## Overview
Scraped book records from `books.toscrape.com` across catalog pages using Python (`requests`, `BeautifulSoup`, `pandas`) and exported the collected data into a CSV file.

## Challenges & Solutions
- **Restricted Mode & Path Setup:** Opened the working folder in VS Code and trusted the workspace so scripts and outputs run smoothly in the local directory.
- **Variable Naming Typo:** Fixed a typo in `category_map` before running the script so category mapping worked cleanly.
- **Pagination & Category Mapping:** Built a category URL map from the sidebar and iterated through catalog pages while checking HTTP status codes to collect records reliably.