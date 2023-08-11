from django.urls import path
from .views import login_user,logout_user
from . import views


 
urlpatterns = [
    path('index', views.index, name='index'),
    path('list_and_display/', views.list_and_display_tables, name='list_and_display_tables'),
    path('display/<str:table_name>/', views.display_table, name='display_table'),
    path('',views.login_user,name="login_user"),
    path('logout_user',views.logout_user,name="logout_user"),
    path('profile', views.profile, name="profile"),


]

