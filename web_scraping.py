import requests
from bs4 import BeautifulSoup
import mysql.connector

# Le reste de votre code...


# Function to connect to the MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",    
        password="",
        database="test_scrap"
    )

# Function to insert data into the MySQL database
def insert_data_to_mysql(connection, title, link, image, date_ajou):
    cursor = connection.cursor()
    query = "INSERT INTO scraping_data (title, link, image, date_ajout) VALUES (%s, %s, %s, %s)"
    data = (title, link, image, date_ajou)
    cursor.execute(query, data)
    connection.commit()
    cursor.close()

# Scraping the website
l_titre = []
l_lien = []
l_images = []
date_ajou = []

result = requests.get("https://veille-transitionenergetique.fr/")
src = result.content
soup = BeautifulSoup(src, "lxml")

titre = soup.find_all("h3", {"class": "slide-entry-title entry-title"})
lien = soup.find_all("h3", {"class": "slide-entry-title entry-title"})
image = soup.find_all("img", {"class": "attachment-portfolio size-portfolio wp-post-image"})

for i in range(len(titre)):
    l_titre.append(titre[i].text)
    l_lien.append(lien[i].find("a").attrs['href'])

for ph in image:
    link_image = ph["src"]
    l_images.append(link_image)

for link in l_lien:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    date = soup.find("time", {"class": "date-container minor-meta updated"})
    if date is not None:
        date_ajou.append(date.text)


# Store the data in the MySQL database
connection = connect_to_mysql()
for i in range(len(l_titre)):
    insert_data_to_mysql(connection, l_titre[i], l_lien[i], l_images[i],date_ajou[i])

connection.close()

