# Whenu (currently under development) `v 0.05`
A web application to ctrl-f through university dining hall menus. Currently functional for the UCLA dining hall menus.

### Description
Whenu is a flask app hosted on aws to allow students to search the week's dining hall menu for certain dishes to figure out when and where they will be served. It uses Beautiful Soup 4 to scrape the dining hall menus and an SQL database to store the gathered data. The entire project is hosted on an EC2 instance which is up 24/7.

### In Development
* launch
* integration with other university dining halls
* backend redesign

### Change log
`v 0.05`
* further sanitized inputs to prevent unexpected outputs

`v 0.04`
* moved app onto an EC2 instance
* implemented scheduled tasks to add new menu items

`v 0.03`
* moved app over to AWS Elastic Beanstalk to support more server connections

`v 0.02`
* a functioning application hosted on Heroku
* implemented SQL database using SQLAlchemy to store menu items ahead of time to reduce loading time
* menus can be updated via script that need to be manually run
* sanitizes inputs to prevent SQL injection

`v 0.01`
* a fully implemented web scraper gathers all the food items and returns data in a json response
