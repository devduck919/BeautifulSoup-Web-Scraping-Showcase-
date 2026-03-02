import pytest
from project import System, Author, Quote
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock

class TestGetTitle:
    def test_returns_correct_title(self, mock_system):
        soup = BeautifulSoup(MOCK_HTML_PAGE, "lxml")
        assert mock_system.get_title(soup) == "Quotes to Scrape"

class TestGetQuotes:
    def test_new_author_added_to_dict(self, populated_system):
        assert "Albert Einstein" in populated_system.authors
        assert "J.K. Rowling" in populated_system.authors

    def test_author_object_type(self, populated_system):
        assert isinstance(populated_system.authors["Albert Einstein"], Author)

    def test_duplicate_author_quotes_appended(self, populated_system):
        """Einstein appears twice in the mock HTML — should have 2 quotes."""
        einstein = populated_system.authors["Albert Einstein"]
        assert len(einstein.quotes) == 2

    def test_unique_author_has_one_quote(self, populated_system):
        rowling = populated_system.authors["J.K. Rowling"]
        assert len(rowling.quotes) == 1

    def test_quote_object_type(self, populated_system):
        einstein = populated_system.authors["Albert Einstein"]
        assert all(isinstance(q, Quote) for q in einstein.quotes)

    def test_quote_tags_are_set(self, populated_system):
        einstein = populated_system.authors["Albert Einstein"]
        assert isinstance(einstein.quotes[0].tags, set)

    def test_quote_tags_correct(self, populated_system):
        einstein = populated_system.authors["Albert Einstein"]
        assert einstein.quotes[0].tags == {"change", "deep-thoughts"}

    def test_author_about_link(self, populated_system):
        einstein = populated_system.authors["Albert Einstein"]
        assert "/author/Albert-Einstein" in einstein.about

class TestStartSystem:
    def test_start_system_returns_system_instance(self):
        """Patches requests.get so no real HTTP call is made."""
        mock_response = MagicMock()
        mock_response.text = MOCK_HTML_PAGE

        with patch("project.quotes_to_scrape.requests.get", return_value=mock_response) as mock_get:
            system = System.start_system()

        assert isinstance(system, System)

    def test_start_system_makes_10_requests(self):
        mock_response = MagicMock()
        mock_response.text = MOCK_HTML_PAGE

        with patch("project.quotes_to_scrape.requests.get", return_value=mock_response) as mock_get:
            System.start_system()

        assert mock_get.call_count == 10

    def test_start_system_website_name_set(self):
        mock_response = MagicMock()
        mock_response.text = MOCK_HTML_PAGE

        with patch("project.quotes_to_scrape.requests.get", return_value=mock_response):
            system = System.start_system()

        assert system.website_name == "Quotes to Scrape"

  

MOCK_HTML_PAGE = """
<html>
  <head><title>Quotes to Scrape</title></head>
  <body>
    <div class="quote">
      <span class="text" itemprop="text">The world as we have created it...</span>
      <small class="author" itemprop="author">Albert Einstein</small>
      <a href="/author/Albert-Einstein">about</a>
      <a class="tag">change</a>
      <a class="tag">deep-thoughts</a>
    </div>
    <div class="quote">
      <span class="text" itemprop="text">It is our choices that show what we truly are.</span>
      <small class="author" itemprop="author">J.K. Rowling</small>
      <a href="/author/J-K-Rowling">about</a>
      <a class="tag">choices</a>
    </div>
    <div class="quote">
      <span class="text" itemprop="text">The only way to do great work is to love what you do.</span>
      <small class="author" itemprop="author">Albert Einstein</small>
      <a href="/author/Albert-Einstein">about</a>
      <a class="tag">work</a>
    </div>
  </body>
</html>
                """