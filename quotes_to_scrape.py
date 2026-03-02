from bs4 import BeautifulSoup
import requests
import pytest 
import random
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process <-- Paste if Permission is denied
#quote_text = quote.find("span",class_="text").text
#author = quote.find("small",class_="author").text
def main():
    system:System = System.start_system()
    while True:
        print(f"Welcome to {system.website_name}!",
                "1) Search Authors",
                "2) Find Quotes",
                "3) Exit",sep="\n")
        
        option = input("Please choose an option: ")

        match option:
            case "1":
                print(system.search_author())
            case "2":
                print(system.random_quote())
            case "3":
                exit()
            case _:
                print("Invalid input, Try Again")

class System:
    def __init__(self):
        self.website_name = "" # name of website
        self.authors:dict = {} # author names --> Author()
    
    @classmethod
    def start_system(cls) -> System: 
        system = cls() # <- We will populate this cls with Authors() containing Quote()
        for page_num in range(1,11): # <- Website has 10 pages in total 
            html_text = requests.get(f"https://quotes.toscrape.com/page/{page_num}/").text # <- Each pass we grab the page # html code
            soup = BeautifulSoup(html_text,'lxml') # <- BS Object to have access to .find and .find_all functions
            if page_num == 1: 
                system.website_name = system.get_title(soup) 
            quote_cells = soup.find_all("div", class_="quote") 
            for cell in quote_cells: # <- call cls function to extract quote vals to create Author/Quote objects
                system.get_quotes(cell)
        return system # <- Return a populated system

    def get_title(self,soup:BeautifulSoup) -> str:
        return soup.find("title").text # <- Finds first instance of title 

    def get_quotes(self,quote_cell:str,URL="https://quotes.toscrape.com/"): 
        author = quote_cell.find("small", class_="author",itemprop="author").text # <- Grabs author name 
        text = quote_cell.find("span",class_="text", itemprop="text").text # <- Grabs actual quote text
        about_link = URL + quote_cell.find("a", href=lambda h: h and "/author/" in h)["href"] # <- Finds about link for author
        tags = set(tag.text for tag in quote_cell.find_all("a",class_="tag")) # <- Puts all tags about quote in a set

        if author not in self.authors: # <- Author is new, create a new author object
            self.authors[author] = Author(author,about_link,Quote(author,text,tags)) 
        else: # <- Author already exists, append quote to their list of quotes
            self.authors[author].quotes.append(Quote(author,text,tags))
    
    def search_author(self) -> str:
        query = input("Enter Author Name: ").strip().lower() # <- we will ignore case sensitivity 
        matches = {name:author for name, author in self.authors.items() if query in name.lower()} # <-- dict comp for catching author object with query in name

        if not matches:
            return f"No Authors matching {query}" # <- dict was empty, no matches were found 
        return "\n".join(str(author) for author in matches.values()) # <- return a list or singleton author object 
    
    def random_quote(self) -> str:
        query = input("Enter author name (or 'any' for random): ").strip().lower() 
        if query == "any" or query == "": # <- if true user wants random quote from random author
            author = random.choice(list(self.authors.values())) # <- assign author a random Author()
        else:
            matches = [author for name, author in self.authors.items() if query in name.lower()] # <- assign Author object if name is found in key
            if not matches:
                return f"No Authors found matching '{query}'"
            author = random.choice(matches) # <- Choose a random author in the list of author objects
        return str(random.choice(author.quotes))  # <- Return that authors random quote __str__ 
      
class Author:
    def __init__(self,name,about,quote):
        self.name:str = name
        self.about:str = about
        self.quotes:list = [quote]
    
    def __str__(self):
        return f"Name: {self.name} About Author: {self.about} Quotes: {len(self.quotes)}"
    
class Quote:
    def __init__(self,author,text,tags):
        self.author_name:str = author
        self.text:str = text
        self.tags:set = tags

    def __str__(self):
        return f"{self.text} by: {self.author_name} tags: {self.tags}"
    

    

if __name__ == "__main__":
    main()



