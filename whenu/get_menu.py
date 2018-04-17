import requests
from bs4 import BeautifulSoup
import datetime

#base menu url
BASE_URL = 'http://menu.dining.ucla.edu/Menus/'
#names of dining halls to check
HALLS = ['Covel', 'DeNeve', 'FeastAtRieber', 'BruinPlate']
HALL_NAMES = {'Covel': 'Covel', 'DeNeve': 'DeNeve', 'FeastAtRieber': 'Feast At Rieber', 'BruinPlate': 'Bruin Plate'}
TIMES = ['Breakfast', 'Dinner', 'Lunch']

#get a soup to parse the menu data
def getMenuSoup(hall, date, time):
    url = BASE_URL + hall + "/" + date + "/" + time
    source_code = requests.get(url)
    source_text = source_code.text
    soup = BeautifulSoup(source_text, "html.parser")
    return soup

#grab the html elements corresponding to menu items
def get_menu_items(soup):
    items = soup.find_all("a", {"class":"recipelink"})
    return items

#compiles names of dishes into a list
def get_item_names(list):
    ret = []
    for item in list:
        ret.append(item.string)
    return ret

#a function to get the occurances of a dish within the next length number of days
def scrape(date):
    #this is the list we will use to keep track of all the occurances
    data = []
    #iterate through each menu
    for hall in HALLS:
        for time in TIMES:
            #get a list of all menu item names
            names = get_item_names(get_menu_items(getMenuSoup(hall, date, time)))
            #iterate through all the item names
            for name in names:
                #gather data on the date, location, and name of dish
                d = {}
                d['date'] = date
                d['location'] = HALL_NAMES[hall]
                d['dish'] = name
                d['time'] = time
                #and add it to the main data list
                data.append(d)
    #return the final object
    return data

def scrape_week():
    date = datetime.datetime.now()
    #this is the list we will use to keep track of all the occurances
    data = []
    for i in range(7):
        #iterate through each menu
        for hall in HALLS:
            for time in TIMES:
                #get a list of all menu item names
                names = get_item_names(get_menu_items(getMenuSoup(hall, date.strftime('%Y-%m-%d'), time)))
                #iterate through all the item names
                for name in names:
                    #gather data on the date, location, and name of dish
                    d = {}
                    d['date'] = date.strftime('%A, %B %d, %Y')
                    d['location'] = HALL_NAMES[hall]
                    d['dish'] = name
                    d['time'] = time
                    #and add it to the main data list
                    data.append(d)
        date = date + datetime.timedelta(1)
    #return the final object
    return data

def initial_scrape():
    date = datetime.datetime.now()
    #this is the list we will use to keep track of all the occurances
    data = []
    for i in range(7):
        #iterate through each menu
        date_halls = []
        for hall in HALLS:
            hall_time = []
            for time in TIMES:
                time_food = []
                #get a list of all menu item names
                names = get_item_names(get_menu_items(getMenuSoup(hall, date.strftime('%Y-%m-%d'), time)))
                #iterate through all the item names
                for name in names:
                    #gather data on the date, location, and name of dish
                    d = {}
                    d['date'] = date.strftime('%A, %B %d, %Y')
                    d['location'] = HALL_NAMES[hall]
                    d['dish'] = name
                    d['time'] = time
                    #and add it to the main data list
                    time_food.append(d)
                t = {}
                t['name'] = time
                t['foods'] = time_food
                hall_time.append(t)
            h = {}
            h['name'] = HALL_NAMES[hall]
            h['times'] = hall_time
            date_halls.append(h)
        d = {}
        d['name'] = date.strftime('%A, %B %d, %Y')
        d['locations'] = date_halls
        data.append(d)
        date = date + datetime.timedelta(1)
    #return the final object
    return data

def scrape_next_week():
    date = datetime.datetime.now()
    #this is the list we will use to keep track of all the occurances
    data = []
    for i in range(6):
        date = date + datetime.timedelta(1)
    #iterate through each menu
    for hall in HALLS:
        for time in TIMES:
            #get a list of all menu item names
            names = get_item_names(get_menu_items(getMenuSoup(hall, date.strftime('%Y-%m-%d'), time)))
            #iterate through all the item names
            for name in names:
                #gather data on the date, location, and name of dish
                d = {}
                d['date'] = date.strftime('%A, %B %d, %Y')
                d['location'] = HALL_NAMES[hall]
                d['dish'] = name
                d['time'] = time
                #and add it to the main data list
                data.append(d)
    #return the final object
    return data

#running tests to compare runtimes
if __name__ == '__main__':
    #start = timeit.default_timer()
    print(initial_scrape())
    #stop = timeit.default_timer()
    #print(stop - start)
