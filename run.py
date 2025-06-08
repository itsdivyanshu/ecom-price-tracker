from app import create_app
from app.tasks.price_tracker import setup_scheduler

app = create_app()
 
if __name__ == '__main__':
    setup_scheduler(app)
    app.run(debug=True) 