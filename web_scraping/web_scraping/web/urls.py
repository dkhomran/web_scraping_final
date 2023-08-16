from django.urls import path
from .views import login_user,logout_user
from . import views
from django.contrib.auth import views as auth_views
from .views import ScrapingView
 
urlpatterns = [
    path('index', views.index, name='index'),
    path('list_and_display/', views.list_and_display_tables, name='list_and_display_tables'),
    path('display/<str:table_name>/', views.display_table, name='display_table'),
    path('',views.login_user,name="login_user"),
    path('logout_user',views.logout_user,name="logout_user"),
    path('profile', views.profile, name="profile"),
    path('scrape/', ScrapingView.as_view(), name='scrape'),
 
    path('historique/<str:table_name>/', views.display_historique, name='display_historique'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

