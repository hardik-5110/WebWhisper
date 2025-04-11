import requests
from bs4 import BeautifulSoup

def scrape_website(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract main content only - simple fallback
    text = soup.get_text(separator='\n', strip=True)
    return text