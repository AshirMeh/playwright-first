import pandas as pd
from sqlalchemy import create_engine
import csv

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

def write_to_csv( quotes: list[dict]):
        print("Writing data to CSV...")
        df = pd.DataFrame(quotes)
        df.to_csv("quotes.csv", index=False)