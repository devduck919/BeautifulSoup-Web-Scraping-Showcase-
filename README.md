# Quotes Scraper 📚

A Python web scraper that collects quotes, authors, and tags from [quotes.toscrape.com](https://quotes.toscrape.com) and lets you search and explore them interactively.

---

## Features

- **Scrapes all 10 pages** of quotes on startup, storing authors and their quotes in memory
- **Search authors** by name — supports partial and case-insensitive matching (e.g. `"albert"` matches `"Albert Einstein"`)
- **Random quote** — retrieve a random quote from a specific author, or pass `"Any"` / leave blank for a completely random quote from any author
- **Structured data** — each author stores their name, about page link, and full list of quotes; each quote stores its text, author, and tags

---

## Project Structure

```
quotes-scraper/
├── main.py          # Scraper logic, System, Author, and Quote classes
├── test_main.py     # Pytest tests for search and random quote methods
├── requirements.txt
└── README.md
```

---

## Installation

```bash
pip install -r requirements.txt
```

**requirements.txt**
```
requests
beautifulsoup4
lxml
pytest
```

---

## Usage

```bash
python main.py
```

The system scrapes all pages on startup, then prompts you to search for authors or retrieve random quotes.

---

## Running Tests

```bash
pytest test_main.py -v
```
