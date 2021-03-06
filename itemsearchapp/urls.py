"""itemsearchapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from itemsearchapp.views import home
from itemsearchapp.views import amazonsearch
from itemsearchapp.views import dbsearch
from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.home, name='home'),
    path('amazonsearch/', views.amazonsearch, name='amazonsearch'),
    path('dbsearch/', views.dbsearch, name='dbsearch'),
    path('track/', views.track_item, name='track_item'),
    path('price_history/', views.price_history, name='price_history')
]
