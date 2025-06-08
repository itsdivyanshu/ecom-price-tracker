# E-commerce Price Tracker

A sophisticated web application that tracks product prices across multiple e-commerce platforms and notifies users of price drops. Built with Python, Flask, BeautifulSoup, and SQLite.

## Features

- 🔍 **Multi-Platform Price Tracking**: Track prices from Amazon, Flipkart, and other major e-commerce platforms
- 📊 **Price History Visualization**: Interactive charts showing price trends over time
- 🔔 **Price Drop Notifications**: Get email alerts when prices drop below your target
- 👤 **User Authentication**: Secure user accounts to manage tracked products
- 📱 **Responsive Design**: Modern UI that works seamlessly on desktop and mobile
- 📈 **Data Analytics**: Historical price data and price drop statistics

## Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Web Scraping**: BeautifulSoup4, Requests
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Visualization**: Chart.js
- **Authentication**: Flask-Login
- **Task Queue**: APScheduler for periodic price checks

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ecom-price-tracker.git
   cd ecom-price-tracker
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. Initialize the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

Visit `http://localhost:5000` to access the application.

## Project Structure

```
ecom-price-tracker/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── scrapers/
│   ├── static/
│   └── templates/
├── migrations/
├── tests/
├── config.py
├── requirements.txt
└── run.py
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
