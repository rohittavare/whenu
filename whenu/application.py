# app.py

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import datetime
from apscheduler.triggers.interval import IntervalTrigger
from get_menu import scrape_week, scrape_next_week

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'SECRET'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    location = db.Column(db.String(60), index=True, unique=False)
    date = db.Column(db.String(120), index=True, unique=False)
    time = db.Column(db.String(10), index=True, unique=False)

    def __repr__(self):
        return self.name + ' ' + self.location + ' ' + self.date

def init_menu():
    items = scrape_week()
    for item in items:
        f = Food(name=item['dish'], location=item['location'], date=item['date'], time=item['time'])
        db.session.add(f)
        db.session.commit()

def change_menu():
    add_menu()
    remove_menu()

def add_menu():
    items = scrape_next_week()
    for item in items:
        f = Food(name=item['dish'], location=item['location'], date=item['date'], time=item['time'])
        db.session.add(f)
        db.session.commit()

def remove_menu():
    date = datetime.datetime.now()
    date = date - datetime.timedelta(1)
    date_string = date.strftime('%A, %B %d, %Y')
    food_to_remove = Food.query.filter_by(date=date_string).all()
    for food in food_to_remove:
        db.session.delete(food)
        db.session.commit()

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/search/')
def search():
    query = request.args.get('food')
    if(all(x.isalnum() or x.isspace() for x in query)):
        return render_template('menu.html', Food = Food.query.filter(Food.name.ilike('%' + query + '%')))
    else:
        return render_template('menu.html')

def initialize():
    print("creating db...")
    db.create_all()
    print("Done.")
    print("initializing menu...")
    init_menu()
    print("Done.")

if __name__ == '__main__':
    initialize()
