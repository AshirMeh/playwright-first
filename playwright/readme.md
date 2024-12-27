This project is a Python-based web scraper that extracts quotes from Quotes to Scrape using Playwright. It fetches quotes, author information, and associated tags from different categories, then stores the data into a CSV file.
Features

    Scrapes quotes from the "Quotes to Scrape" website.
    Collects author information such as name, date of birth, location, and bio.
    Retrieves tags associated with each quote.
    Handles pagination to fetch quotes from multiple pages.
    Saves the scraped data into a CSV file.

Requirements

    Python 3.12+ (or any compatible version)
    Playwright library (for web scraping)
    A CSV writer helper for saving the data into a CSV file

Installation

    Clone this repository to your local machine.

git clone https://github.com/yourusername/quotes-scraper.git
cd quotes-scraper

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate

Install the required dependencies:

pip install playwright
pip install -r requirements.txt

Install Playwright dependencies:

    playwright install

Usage

    Set up the writer_helpers.py file:
        Ensure you have the write_to_csv function implemented to save the scraped data to a CSV file. This will be used to write the collected quotes, author information, and tags.

    Run the scraper:

    Once everything is set up, you can run the script with:

    python scraper.py

    The scraper will:
        Fetch the top categories of quotes.
        Scrape quotes from each category.
        Fetch additional author information for each quote.
        Save the scraped data to a CSV file.

Project Structure

quotes-scraper/
│
├── scraper.py            # Main scraping script
├── writer_helpers.py     # Helper functions for saving to CSV/SQL
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

Example CSV Output

The CSV file generated will have the following columns:

    quote: The text of the quote.
    author: The name of the author.
    location: The location where the author was born.
    description: A brief description of the author.
    author_dob: The author's date of birth.
    tags: A list of tags related to the quote.

Debugging

You can set breakpoints and interact with the program using Python's pdb (Python Debugger). To do so, use pdb.set_trace() where you want the program to pause.

To continue the program from a paused state in pdb, type continue or c.
Contributing

Feel free to fork this repository and submit pull requests. Contributions are welcome!
License

This project is licensed under the MIT License - see the LICENSE file for details.
