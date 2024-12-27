import json
import pdb
import pdb
from writer_helpers import write_to_csv, write_to_sql
from playwright.sync_api import sync_playwright



quotes: list = []
categories: dict[str: str] = {}
base_url: str = "https://quotes.toscrape.com"

def fetch_top_categories(page):
        print("Fetching top categories...")
        tags = page.locator(".tag-item a").all()[:10]
        for tag in tags:
            categories[tag.inner_text()] = tag.get_attribute("href")
        print(categories)

def fetch_quotes(page):
    for key in categories:
        page.goto(f"{base_url}{categories[key]}")
        print(f"Scraping category: {base_url}{categories[key]}...")
        quote_elements = page.locator(".quote").all()

        for quote_element in quote_elements:
            auth_info = fetch_author_info(page, f"{base_url}{quote_element.locator("span a").get_attribute("href")}")
            quotes.append({
                        "quote": quote_element.locator(".text").inner_text(),
                        "author": quote_element.locator(".author").inner_text(),
                        "location": auth_info["location"],
                        "description": auth_info["bio"],
                        "author_dob": auth_info["dob"],
                        "tags": [tag.inner_text() for tag in quote_element.locator(".tags .tag").all()],
                        
                        })
        next_button = page.locator(".pager .next a")
        if next_button.count() == 0:
            break
        next_button.click()
        page.wait_for_load_state("load")

def fetch_author_info(page, url):
    page.goto(url)
    print(f"Fetching author info: {url}...")
    #pdb.set_trace()
    author_title = page.locator(".author-title").inner_text()
    dob = page.locator(".author-born-date").inner_text()
    location = page.locator(".author-born-location").inner_text()
    description = page.locator(".author-description").inner_text()
    page.go_back()


    return {
        "name": author_title,
        "dob": dob,
        "location": location,
        "bio": description
    }


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(base_url)
        fetch_top_categories(page)
        fetch_quotes(page)

        browser.close()

    write_to_csv(quotes)

run()