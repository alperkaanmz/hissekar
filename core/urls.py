from . import views
from django.urls import path

appname = 'app'

urlpatterns = [
    path('', views.marketcap, name='marketcap'),
    path('marketcap/', views.marketcap, name='marketcap'),
    path('profile/<str:symbol>/', views.profile, name='profile'),
    path('datatables/', views.datatables_improved, name='datatables'),
]