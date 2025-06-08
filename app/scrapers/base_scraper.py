import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class BaseScraper(ABC):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    @abstractmethod
    def extract_price(self, soup):
        """Extract price from the soup object"""
        pass
    
    @abstractmethod
    def extract_name(self, soup):
        """Extract product name from the soup object"""
        pass
    
    @abstractmethod
    def extract_image_url(self, soup):
        """Extract product image URL from the soup object"""
        pass
    
    def get_soup(self, url):
        """Get BeautifulSoup object from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {str(e)}")
            return None
    
    def clean_price(self, price_str):
        """Clean price string and convert to float"""
        if not price_str:
            return None
        
        # Remove currency symbols and other characters
        price_str = ''.join(filter(lambda x: x.isdigit() or x == '.', price_str))
        try:
            return float(price_str)
        except ValueError:
            return None
    
    def get_platform(self, url):
        """Get platform name from URL"""
        domain = urlparse(url).netloc
        if 'amazon' in domain:
            return 'amazon'
        elif 'flipkart' in domain:
            return 'flipkart'
        else:
            return 'unknown'
    
    def scrape(self, url):
        """Main scraping method"""
        soup = self.get_soup(url)
        if not soup:
            return None
        
        return {
            'name': self.extract_name(soup),
            'price': self.extract_price(soup),
            'image_url': self.extract_image_url(soup),
            'platform': self.get_platform(url)
        } 