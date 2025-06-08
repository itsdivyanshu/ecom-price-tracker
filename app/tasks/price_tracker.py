from app import db, scheduler
from app.models.product import Product, PriceHistory
from app.scrapers.scraper_factory import ScraperFactory
from flask_mail import Message
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def check_prices():
    """Check prices for all tracked products"""
    logger.info("Starting price check task")
    products = Product.query.all()
    
    for product in products:
        try:
            # Scrape current price
            product_data = ScraperFactory.scrape_product(product.url)
            if not product_data or product_data['price'] is None:
                logger.warning(f"Could not fetch price for product {product.id}")
                continue
            
            new_price = product_data['price']
            
            # Update product if price changed
            if product.current_price != new_price:
                product.update_price(new_price)
                
                # Create price history entry
                history = PriceHistory(
                    product_id=product.id,
                    price=new_price
                )
                db.session.add(history)
                
                # Check if notification needed
                if product.should_notify():
                    send_price_alert(product)
            
            product.last_checked = datetime.utcnow()
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error checking price for product {product.id}: {str(e)}")
            continue

def send_price_alert(product):
    """Send price drop notification email"""
    from app import mail
    from flask import current_app, url_for
    
    try:
        msg = Message(
            subject=f"Price Drop Alert for {product.name}",
            recipients=[product.user.email],
            body=f"""
            Good news! The price of {product.name} has dropped to {product.current_price}!
            
            Your target price was: {product.target_price}
            Current price: {product.current_price}
            
            View the product: {product.url}
            
            Track more products at: {url_for('main.dashboard', _external=True)}
            """,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        logger.info(f"Price alert sent for product {product.id}")
    
    except Exception as e:
        logger.error(f"Error sending price alert for product {product.id}: {str(e)}")

def setup_scheduler(app):
    """Setup the price checking scheduler"""
    with app.app_context():
        # Schedule price checking job
        interval = app.config.get('PRICE_CHECK_INTERVAL', 60)  # Default to 60 minutes
        scheduler.add_job(
            func=check_prices,
            trigger='interval',
            minutes=interval,
            id='price_checker',
            replace_existing=True
        ) 