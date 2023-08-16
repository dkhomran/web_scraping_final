from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User,auth
from django.contrib import messages
from web_scraping import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.views.generic.base import View
import requests
from bs4 import BeautifulSoup
import mysql.connector

@login_required(login_url='login_user')
def index(request):
    url = None
    scraped_data = None

    if request.method == 'POST':
        url = request.POST.get('url')
        ScrapingView().scrape_website_and_insert_data()
        scraped_data = ScrapingView().get_scraped_data()

    return render(request, 'index.html', {'url': url, 'scraped_data': scraped_data})



def list_and_display_tables(request):
    # Récupérer la liste des noms de tables et leurs dates de création
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name, create_time FROM information_schema.TABLES WHERE table_schema = %s", [connection.settings_dict['NAME']])
        table_info = cursor.fetchall()

    # Filtrer les informations pour inclure uniquement 'solar_data' et 'scraping_data'
    filtered_table_info = [(table_name, create_time) for table_name, create_time in table_info if table_name in ['solar_data', 'scraping_data']]

    return render(request, 'list_and_display_tables.html', {'table_info': filtered_table_info})



# def display_table(request, table_name):
#     with connection.cursor() as cursor:
#         sort_column = request.GET.get('sort', 'date_ajout')
#         sort_order = request.GET.get('order', 'desc')

#         order_symbol = '-' if sort_order == 'desc' else ''

#         query = f"SELECT * FROM {table_name} ORDER BY {order_symbol}{sort_column}"
        
#         search_date_start = request.GET.get('search_date_start')
#         search_date_end = request.GET.get('search_date_end')
        
#         if search_date_start and search_date_end:
#             start_date = datetime.strptime(search_date_start, '%Y-%m-%d')
#             end_date = datetime.strptime(search_date_end, '%Y-%m-%d')
            
#             query = f"SELECT * FROM {table_name} WHERE date_ajout BETWEEN '{start_date.date()}' AND '{end_date.date()}' ORDER BY {order_symbol}{sort_column}"
        
#         cursor.execute(query)

#         columns = [col[0] for col in cursor.description]
#         data = cursor.fetchall()

#         paginator = Paginator(data, 7)  # Change 10 to the number of items per page you want
#         page_number = request.GET.get('page')
#         page_data = paginator.get_page(page_number)

#     return render(request, 'display_table.html', {
#         'table_name': table_name,
#         'columns': columns,
#         'data': page_data,
#     })

def display_table(request, table_name):
    with connection.cursor() as cursor:
        sort_column = request.GET.get('sort', 'date_ajout')
        sort_order = request.GET.get('order', 'desc')
        order_symbol = '-' if sort_order == 'desc' else ''

        search_date_range = request.GET.get('date_range')
        
        if search_date_range:
            start_date_str, end_date_str = search_date_range.split(' au ')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            query = f"SELECT * FROM {table_name} WHERE date_ajout BETWEEN '{start_date.date()}' AND '{end_date.date()}' ORDER BY {order_symbol}{sort_column}"
        else:
            query = f"SELECT * FROM {table_name} ORDER BY {order_symbol}{sort_column}"

        cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()

        paginator = Paginator(data, 7)  # Change 7 to the number of items per page you want
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)

    return render(request, 'display_table.html', {
        'table_name': table_name,
        'columns': columns,
        'data': page_data,
    })


# def display_table(request, table_name):
#     with connection.cursor() as cursor:
#         sort_column = request.GET.get('sort', 'date_ajout')
#         sort_order = request.GET.get('order', 'desc')

#         order_symbol = '-' if sort_order == 'desc' else ''

#         query = f"SELECT * FROM {table_name} ORDER BY {order_symbol}{sort_column}"
        
#         search_date_start = request.GET.get('search_date_start')
#         search_date_end = request.GET.get('search_date_end')
        
#         if search_date_start and search_date_end:
#             start_date = datetime.strptime(search_date_start, '%Y-%m-%d')
#             end_date = datetime.strptime(search_date_end, '%Y-%m-%d')
            
#             query = f"SELECT * FROM {table_name} WHERE date_ajout BETWEEN '{start_date.date()}' AND '{end_date.date()}' ORDER BY {order_symbol}{sort_column}"
        
#         cursor.execute(query)

#         columns = [col[0] for col in cursor.description]
#         data = cursor.fetchall()

#         paginator = Paginator(data, 7)  # Change 10 to the number of items per page you want
#         page_number = request.GET.get('page')
#         page_data = paginator.get_page(page_number)

#     return render(request, 'display_table.html', {
#         'table_name': table_name,
#         'columns': columns,
#         'data': page_data,
#     })


def display_historique(request, table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM date_up ORDER BY timestamp DESC")
        table_content = cursor.fetchall()

    return render(request, 'display_historique.html', {'table_content': table_content, 'table_name': table_name})



def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin:index')  # Redirect to admin dashboard
        else:
            return redirect('index')  # Redirect to the index page

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_staff:
                return redirect('admin:index')  # Redirect to admin dashboard
            else:
                return redirect('index')  # Redirect to the index page
        else:
            messages.info(request, 'Invalid Username or password')
            return redirect('login_user')
    else:
        return render(request, "login.html")




def logout_user(request):
    auth.logout(request)
    return redirect('login_user')

 


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Mise à jour des informations utilisateur
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if new_password != '':
            # Vérification du mot de passe actuel
            if not user.check_password(current_password):
                messages.error(request, 'Incorrect current password')
                return redirect('profile')
                if new_password == confirm_password:
                    user.set_password(new_password)
                    update_session_auth_hash(request, user) # Mettre à jour la session pour éviter la déconnexion
    
        user.save()
        messages.success(request, 'Profile updated successfully')

    return render(request, 'profile.html', {'user': user})




class ScrapingView(View):

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

    def connect_to_mysql(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test_scrap"
        )

    def create_date_up_table(self, connection):
        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS date_up (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME
            )
        """
        cursor.execute(create_table_query)
        cursor.close()

    def insert_timestamp(self, connection):
        cursor = connection.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO date_up (timestamp) VALUES (%s)"
        data = (timestamp,)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()

    def scrape_website_and_insert_data(self):
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

        connection = self.connect_to_mysql()
        self.create_date_up_table(connection)
        self.insert_timestamp(connection)

        cursor = connection.cursor()
        for i in range(len(l_title)):
            day, month_name, year = date_ajou[i].split(' ')
            month = self.french_month_mapping.get(month_name.lower(), 1)
            formatted_date = f'{year}-{month:02d}-{int(day):02d}'
            query = "INSERT INTO solar_data (title, link, image, date_ajout) VALUES (%s, %s, %s, %s)"
            data = (l_title[i], l_lien[i], l_images[i], formatted_date)
            cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()

    def get_scraped_data(self):
        connection = self.connect_to_mysql()
        cursor = connection.cursor()
        query = "SELECT title, link, image, date_ajout FROM solar_data"
        cursor.execute(query)
        scraped_data = []
        for row in cursor.fetchall():
            title, link, image, date_ajout = row
            scraped_data.append({
                'title': title,
                'link': link,
                'image': image,
                'date_ajout': date_ajout,
            })
        cursor.close()
        connection.close()
        return scraped_data

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {'scraping_done': False, 'scraping_logs': []})

    def post(self, request, *args, **kwargs):
        self.scrape_website_and_insert_data()
        return render(request, 'index.html', {'scraping_done': True, 'scraping_logs': []})