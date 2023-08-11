import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import mysql.connector
from datetime import datetime

# Mapping of French month names to numeric values
french_month_mapping = {
    "janvier": 1,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12
}

# Function to connect to the MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test_scrap"
    )

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS solar_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            link VARCHAR(255),
            image VARCHAR(255),
            date_ajout DATE
        )
    """
    cursor.execute(create_table_query)
    cursor.close()

# Function to insert data into the MySQL database
def insert_data_to_mysql(connection, title, link, image, date_ajou):
    cursor = connection.cursor()
    day, month_name, year = date_ajou.split(' ')
    month = french_month_mapping[month_name.lower()]
    formatted_date = f'{year}-{month:02d}-{int(day):02d}'
    query = "INSERT INTO solar_data (title, link, image, date_ajout) VALUES (%s, %s, %s, %s)"
    data = (title, link, image, formatted_date)
    cursor.execute(query, data)
    connection.commit()
    cursor.close()

# Scraping the website
result = requests.get("https://www.encyclopedie-energie.org/recherche/?mot-cle=solar")
src = result.content
soup = BeautifulSoup(src, "lxml")

titles = soup.find_all("div", {"class": "title"})
link = soup.find_all("div", {"class": "image"})
date = soup.find_all("span", {"class": "date_article"})

l_title = []
l_lien = []
l_images = []
date_ajou = []

for i in range(len(titles)):
    l_title.append(titles[i].text)
    date_ajou.append(date[i].text)
    l_images.append(link[i].find("img").attrs['src'])
    l_lien.append(link[i].find("a").attrs['href'])

# Store the data in the MySQL database
connection = connect_to_mysql()
create_table(connection)  # Create the table if it doesn't exist
for i in range(len(l_title)):
    insert_data_to_mysql(connection, l_title[i], l_lien[i], l_images[i], date_ajou[i])

connection.close()