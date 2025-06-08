from .base_scraper import BaseScraper

class AmazonScraper(BaseScraper):
    def extract_price(self, soup):
        """Extract price from Amazon product page"""
        price_element = soup.select_one('.a-price-whole')
        if price_element:
            return self.clean_price(price_element.text)
        
        # Try alternative price elements
        price_element = soup.select_one('#priceblock_ourprice, #priceblock_dealprice')
        if price_element:
            return self.clean_price(price_element.text)
        
        return None
    
    def extract_name(self, soup):
        """Extract product name from Amazon product page"""
        name_element = soup.select_one('#productTitle')
        if name_element:
            return name_element.text.strip()
        return None
    
    def extract_image_url(self, soup):
        """Extract product image URL from Amazon product page"""
        img_element = soup.select_one('#landingImage')
        if img_element and 'src' in img_element.attrs:
            return img_element['src']
        
        # Try alternative image element
        img_element = soup.select_one('#imgBlkFront')
        if img_element and 'src' in img_element.attrs:
            return img_element['src']
        
        return None 