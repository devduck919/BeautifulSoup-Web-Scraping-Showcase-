import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from project import System, Author, Quote

@pytest.fixture
def mock_system():
    return System()

@pytest.fixture
def populated_system():
    system = System()
    soup = BeautifulSoup(MOCK_HTML_PAGE,'lxml')
    for cell in soup.find_all("div",class_="quote"):
        system.get_quotes(cell)
    return system

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