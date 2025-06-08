from datetime import datetime
from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    current_price = db.Column(db.Float)
    target_price = db.Column(db.Float)
    image_url = db.Column(db.String(500))
    platform = db.Column(db.String(50))  # e.g., 'amazon', 'flipkart'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    notify_on_price_drop = db.Column(db.Boolean, default=True)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship with price history
    price_history = db.relationship('PriceHistory', backref='product', lazy='dynamic',
                                  cascade='all, delete-orphan')
    
    def __init__(self, name, url, user_id, target_price=None):
        self.name = name
        self.url = url
        self.user_id = user_id
        self.target_price = target_price
    
    def update_price(self, new_price):
        if self.current_price != new_price:
            self.current_price = new_price
            self.last_checked = datetime.utcnow()
            
            # Create price history entry
            history_entry = PriceHistory(
                product_id=self.id,
                price=new_price
            )
            db.session.add(history_entry)
    
    def should_notify(self):
        return (self.notify_on_price_drop and 
                self.target_price and 
                self.current_price <= self.target_price)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PriceHistory {self.product_id} - {self.price}>' 