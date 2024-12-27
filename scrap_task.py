"""
refactors to be done: implement a class, use URL only once, to ref, dont pass in func call, also check where substrings can
be used instead of using entire f strings
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
from sqlalchemy import create_engine
import json, string
import pdb


class QuoteScrapper():
    

    def __init__(self):
        self.QUOTE_LIST: list[str] = []
        self.CATEGORIES_URLS: list[str] = []
        self.AUTHORS: list[str] = []
        self.TAGS: list[str] = []
        self.AUTHOR_INFO: list[dict] = []
        self.AUTHOR_LINKS: list[str] = []
        self.URL = "https://quotes.toscrape.com"
        self.CATEGORY_NAMES = []
        self.CATEGORIES: str = []


    # we have pagination in our site, so need to get inside a loop
    def fetch_data(self, URL: str, url_path: str, category: str):
        """ """
        page: bool = True
        page_count = 1
        temp_cateory = []

        while page:
            curr_url: str
            try:
                curr_url = f"{ URL }{ url_path }page/{ page_count }/"
                res = requests.get(curr_url)
            except TimeoutError:
                print("can not reach server, timed out")
                print(res.status_code)
                continue

            print(f"Fetching Results .....  scraping: {curr_url}")

            soup = BeautifulSoup(res.text)

            if (
                not soup.find_all("div", {"class": "quote"})
                or soup.find(("div", {"class": "col-md-8"})).text == "No quotes found!"
            ):
                break

            for i in soup.findAll("div", {"class": "tags"}):
                temp_tags: list[list] = []
                try:
                    tags = i.find_all(("a", {"class": "tag"}))
                    for j in tags:
                        temp_tags.append(j.text)
                except:
                    temp_tags.append(None)
                    continue
                self.TAGS.append(", ".join(temp_tags))  

                # breakpoint()

            for i in soup.findAll("div", {"class": "quote"}):
                self.QUOTE_LIST.append(i.find(("span", {"class": "text"})).text)
                self.CATEGORIES.append(category)

            for i in soup.findAll("small", {"class": "author"}):
                self.AUTHORS.append(i.text)

            # author_info
            for i in soup.findAll("div", {"class": "quote"}):
                # could also make a dict for jso format for authinfo
                temp_author_info = []
                a = i.find("a", href=True)
                temp_author_info.append(a["href"])
                self.AUTHOR_LINKS.append(temp_author_info)
                self.fetch_author_info(URL + a["href"])
            
            temp_cateory.append(category)

            # updating page count
            page_count += 1


    def fetch_author_info(self, url: str):
        try:
            res = requests.get(url)
        except TimeoutError:
            print("can not reach server, timed out")
            print(res.status_code)

        soup = BeautifulSoup(res.text, "html.parser")

        for i in soup.findAll("div", {"class": "author-details"}):
            title = (i.find("h3", {"class": "author-title"})).text.strip()
            dob = (i.find("span", {"class": "author-born-date"})).text.strip()
            location = (i.find("span", {"class": "author-born-location"})).text.strip()
            desc = (i.find("div", {"class": "author-description"})).text.strip()
            self.AUTHOR_INFO.append(
                f"TITLE: {title}, dob: {dob}, location: {location}, bio: {desc}"
            )


    # should fetch all the same stuff for every div in each one of the top ten tags, since they are static on everypage
    def top_ten(self, url: str):
        res: str
        try:
            res = requests.get(url)
        except TimeoutError:
            print("can not reach server, timed out")
            print(res.status_code)
        
        print("Initiating top ten tags scrapping.....")

        soup = BeautifulSoup(res.text, "html.parser")

        for i in soup.findAll("div", {"class": "col-md-4 tags-box"}):
            for j in i.findAll("span", {"class": "tag-item"}):
                tags = j.find("a",  href=True)
                self.CATEGORIES_URLS.append(tags["href"])
                self.CATEGORY_NAMES.append(tags.text)


    def write_sql(self):
        """
        writes to mysql, all the scrapped data
        """
        df = pd.DataFrame(
            {
            "quotes": self.QUOTE_LIST,
            "author": self.AUTHORS,
            "authorinfo": self.AUTHOR_INFO, 
            "tags": self.TAGS,
            "category": self.CATEGORIES
            }
            )

        ## mysql.connector method

        # try:
        #     quotesdb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="password123@",
        #     database="my_database"
        #     )
            
        #     print("connection established")

        #     mycursor = quotesdb.cursor()
        #     mycursor.execute("create database if not exists my_quotes")
        #     quotesdb.commit()
        #     print("database created successfully")
        #     mycursor.execute("use my_quotes")
        #     mycursor.execute("CREATE TABLE scraped_quotes (id INT AUTO_INCREMENT PRIMARY KEY, quotes VARCHAR(255), author VARCHAR(255), authorinfo TEXT, tags VARCHAR(255), category VARCHAR(255))")
        #     mycursor.execute()
        # except mysql.connector.Error as err:
        #     print(err)
        
        ## sqlalchemy create engine method ##

        try:
            engine = create_engine(
                "mysql+mysqlconnector://root:Password123!@localhost:3306/quotes"
            )
        except engine.error as e:
            print(f"could not establish a connection with database {e}")

        df.to_sql("scraped_quotes", con=engine, if_exists="replace", index=False)
        print("success !")


    def csv_maker(self):
    # CSV writing alternative if needed for custom format
        fields = ["quote", "author", "author_info", "tags", "category"]
        with open("my_quotes.csv", "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(fields)

            for i in range(len(self.QUOTE_LIST)):
                # Assuming AUTHOR_INFO is a list of dictionaries
                author_info_str = json.dumps(self.AUTHOR_INFO[i]) if self.AUTHOR_INFO else ""
                csv_writer.writerow([self.QUOTE_LIST[i], self.AUTHORS[i], author_info_str, self.TAGS[i], self.CATEGORIES[i]])    
    

if __name__ == "__main__":
    quotes_scrapper = QuoteScrapper()
    quotes_scrapper.top_ten(quotes_scrapper.URL)

    for i, j in enumerate(quotes_scrapper.CATEGORIES_URLS):
        quotes_scrapper.fetch_data(quotes_scrapper.URL, j, quotes_scrapper.CATEGORY_NAMES[i])
    
    quotes_scrapper.write_sql()
