from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.product import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page route"""
    return render_template('main/index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing tracked products"""
    products = Product.query.filter_by(user_id=current_user.id).order_by(Product.created_at.desc()).all()
    return render_template('main/dashboard.html', products=products)

@main.route('/about')
def about():
    """About page route"""
    return render_template('main/about.html') 