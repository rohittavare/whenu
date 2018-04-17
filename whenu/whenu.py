import os
from bs4 import BeautifulSoup
import requests
import re
import datetime
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

def getMenuSoup(hall, date):
    url = "http://menu.dining.ucla.edu" + hall + "/" + date
    source_code = requests.get(url)
    source_text = source_code.text
    soup = BeautifulSoup(source_text, "html.parser")
    return soup

def getHourSoup():
    url = "http://menu.dining.ucla.edu/Hours/"
    source_code = requests.get(url)
    source_text = source_code.text
    soup = BeautifulSoup(source_text, "html.parser")
    return soup

def menu_links(href):
    return href and re.compile("Menus/").search(href)

def get_menu_links(soup):
    links = getHourSoup().find_all(href=menu_links)
    ret = []
    for link in links:
        if re.compile("Menu").search(link.string):
            ret.append(link)
    return ret

def get_hall_name(link):
    if(re.compile('FEAST').search(link.get('href'))):
        return 'Feast'
    elif(re.compile('De Neve').search(link.get('href'))):
        return 'De Neve'
    elif(re.compile('Covel').search(link.get('href'))):
        return 'Covel'
    elif(re.compile('Bruin Plate').search(link.get('href'))):
        return 'Bruin Plate'
    else:
        return 'ToGo'

def get_food():
    date = datetime.datetime.now()
    links = get_menu_links(getHourSoup())
    for link in links:
        list = get_item_names(get_menu_items(getMenuSoup(link.get("href"), "")))
        for food in list:
            add_food(food, get_hall_name(link.get("href")), date.strftime('%Y-%m-%d'))

def add_food(name, hall, date):
    db = get_db()
    db.execute('insert into menu (name, date, hall) values (?, ?, ?)',
               [name, date, hall])
    db.commit()
    print(name + " is added to the db")

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'whenu.db'),
    SECRET_KEY='development key',
    USERNAME='admin'
    PASSWORD='default'
))
app.config.from_envvar('WHENU_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlitedb = connect_db()
    return g.sqlite_db()

@app.teardown_appcontext
def close_db():
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('shema.sql', mode='r') as f:
        db.cursor().execute_script(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('initialized the database.')
    get_food()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.excute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session('logged_in')
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values ( ?, ? )',
                [request.form['title'], request.form[text]])
    db.commit()
    flash('New entry has been added')
    return redirect(url_for('show_entries'))


