from urllib.parse import urlparse
from .amazon_scraper import AmazonScraper
from .flipkart_scraper import FlipkartScraper

class ScraperFactory:
    @staticmethod
    def get_scraper(url):
        """Get appropriate scraper based on URL"""
        domain = urlparse(url).netloc.lower()
        
        if 'amazon' in domain:
            return AmazonScraper()
        elif 'flipkart' in domain:
            return FlipkartScraper()
        else:
            raise ValueError(f"No scraper available for domain: {domain}")
    
    @staticmethod
    def scrape_product(url):
        """Scrape product details using appropriate scraper"""
        scraper = ScraperFactory.get_scraper(url)
        return scraper.scrape(url) 