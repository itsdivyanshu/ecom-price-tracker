from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.product import Product, PriceHistory
from app.scrapers.scraper_factory import ScraperFactory
from datetime import datetime, timedelta

products = Blueprint('products', __name__)

@products.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """Add a new product to track"""
    if request.method == 'POST':
        url = request.form.get('url')
        target_price = request.form.get('target_price')
        
        try:
            # Scrape product details
            product_data = ScraperFactory.scrape_product(url)
            if not product_data:
                flash('Could not fetch product details. Please check the URL.', 'danger')
                return redirect(url_for('products.add_product'))
            
            # Create new product
            product = Product(
                name=product_data['name'],
                url=url,
                user_id=current_user.id,
                current_price=product_data['price'],
                target_price=float(target_price) if target_price else None,
                image_url=product_data['image_url'],
                platform=product_data['platform']
            )
            
            db.session.add(product)
            db.session.commit()
            
            # Add initial price history
            history = PriceHistory(
                product_id=product.id,
                price=product_data['price']
            )
            db.session.add(history)
            db.session.commit()
            
            flash('Product added successfully!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'danger')
            return redirect(url_for('products.add_product'))
    
    return render_template('products/add.html')

@products.route('/<int:product_id>')
@login_required
def view_product(product_id):
    """View product details and price history"""
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get price history for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    price_history = PriceHistory.query.filter_by(product_id=product_id)\
        .filter(PriceHistory.timestamp >= thirty_days_ago)\
        .order_by(PriceHistory.timestamp.asc()).all()
    
    return render_template('products/view.html', product=product, price_history=price_history)

@products.route('/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    """Delete a tracked product"""
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))

@products.route('/<int:product_id>/update', methods=['POST'])
@login_required
def update_product(product_id):
    """Update product target price"""
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    target_price = request.form.get('target_price')
    if target_price:
        product.target_price = float(target_price)
        db.session.commit()
        flash('Target price updated successfully.', 'success')
    
    return redirect(url_for('products.view_product', product_id=product_id))

@products.route('/<int:product_id>/price_history')
@login_required
def price_history(product_id):
    """Get price history data for charts"""
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    days = int(request.args.get('days', 30))
    start_date = datetime.utcnow() - timedelta(days=days)
    
    history = PriceHistory.query.filter_by(product_id=product_id)\
        .filter(PriceHistory.timestamp >= start_date)\
        .order_by(PriceHistory.timestamp.asc()).all()
    
    data = [{
        'date': h.timestamp.strftime('%Y-%m-%d'),
        'price': h.price
    } for h in history]
    
    return jsonify(data) 