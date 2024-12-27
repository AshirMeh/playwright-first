from playwright.sync_api import sync_playwright
import pandas as pd
from sqlalchemy import create_engine
import csv
import json


class QuoteScraper:
    def __init__(self):
        self.quotes: list = []
        self.categories: dict[str: str] = {}
        self.base_url: str = "https://quotes.toscrape.com"

    def fetch_top_categories(self, page):
        print("Fetching top categories...")
        tags = page.locator(".tag-item a").all()[:10]
        for tag in tags:
            self.categories[tag.inner_text()] = tag.get_attribute("href")
        print(self.categories)

    def fetch_quotes(self, page):
        for key in self.categories:
            page.goto(f"{self.base_url}{self.categories[key]}")
            print(f"Scraping category: {self.base_url}{self.categories[key]}...")

            while True:
                quote_elements = page.locator(".quote")
                for quote_element in quote_elements.all():
                    self.quotes.append(quote_element.locator(".text").inner_text())
                    self.authors.append(quote_element.locator(".author").inner_text())
                    tags = [tag.inner_text() for tag in quote_element.locator(".tags .tag").all()]
                    self.tags.append(", ".join(tags))
                    # Fetch author info URL
                    author_url = quote_element.locator("span a").get_attribute("href")
                    self.fetch_author_info(page, f"{self.base_url}{author_url}")

                next_button = page.locator(".pager .next a")
                if next_button.count() == 0:
                    break
                next_button.click()
                page.wait_for_load_state("load")

    def fetch_author_info(self, page, url):
        page.goto(url)
        print(f"Fetching author info: {url}...")
        author_title = page.locator(".author-title").inner_text()
        dob = page.locator(".author-born-date").inner_text()
        location = page.locator(".author-born-location").inner_text()
        description = page.locator(".author-description").inner_text()

        self.author_info.append({
            "name": author_title,
            "dob": dob,
            "location": location,
            "bio": description
        })

    def write_to_csv(self):
        print("Writing data to CSV...")
        data = {
            "quotes": self.quotes,
            "authors": self.authors,
            "tags": self.tags,
            "categories": self.categories
        }
        df = pd.DataFrame(data)
        df.to_csv("quotes.csv", index=False)

    def write_to_sql(self):
        print("Writing data to MySQL...")
        data = {
            "quotes": self.quotes,
            "authors": self.authors,
            "tags": self.tags,
            "categories": self.categories
        }
        df = pd.DataFrame(data)

        try:
            engine = create_engine(
                "mysql+mysqlconnector://root:Password123!@localhost:3306/quotes"
            )
            df.to_sql("scraped_quotes", con=engine, if_exists="replace", index=False)
            print("Data successfully written to MySQL!")
        except Exception as e:
            print(f"Failed to write data to MySQL: {e}")

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(self.base_url)
            self.fetch_top_categories(page)

            for category_url, category_name in zip(self.categories_urls, self.categories):
                self.fetch_quotes(page, category_url, category_name)

            browser.close()

        self.write_to_csv()
        self.write_to_sql()


if __name__ == "__main__":
    scraper = QuoteScraper()
    scraper.run()
