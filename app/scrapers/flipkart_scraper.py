from .base_scraper import BaseScraper

class FlipkartScraper(BaseScraper):
    def extract_price(self, soup):
        """Extract price from Flipkart product page"""
        price_element = soup.select_one('._30jeq3._16Jk6d')  # Flipkart's price class
        if price_element:
            return self.clean_price(price_element.text)
        return None
    
    def extract_name(self, soup):
        """Extract product name from Flipkart product page"""
        name_element = soup.select_one('.B_NuCI')  # Flipkart's product title class
        if name_element:
            return name_element.text.strip()
        return None
    
    def extract_image_url(self, soup):
        """Extract product image URL from Flipkart product page"""
        img_element = soup.select_one('._396cs4')  # Flipkart's main product image class
        if img_element and 'src' in img_element.attrs:
            return img_element['src']
        return None 