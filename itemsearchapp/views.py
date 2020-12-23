from django.shortcuts import render
from itemsearchapp.models import Item
from decimal import Decimal

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import pandas as pd

def home(request):
    return render(request, 'home.html')

def amazonsearch(request):
    if request.method == "POST":
        get_name = request.POST["amazonitemname"]
        data = getItemAmazon(get_name)
        count = 0
        for key, value in data.items():
            Item.objects.create(name=key, price=value[0], image_url=value[1])
            count += 1

    context = {
        "status": get_name,
        "addedcount": count
    }

    return render(request, 'amazonresults.html', context)

def dbsearch(request):
    if request.method == "POST":
        get_name = request.POST["dbitemname"]

    item_obj = Item.objects.filter(name__icontains=get_name)

    context = {
        "items": item_obj
    }

    return render(request, 'dbresults.html', context)

def track_item(request):
    if request.method == "POST":
        track_name = request.Post["track_name"]

    Item.objects.filter(name=track_name).update(isTracked=True)
    item_obj = Item.objects.filter(name_icontains=track_name)
    
    context = {
        "items": item_obj,
        "track_name": track_name
    }

    return render(request, 'dbresults.html', context)

def getItemAmazon(searchname):

    headers = { 
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip', 
        'DNT' : '1', # Do Not Track Request Header 
        'Connection' : 'close'
    }

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get("https://www.amazon.ca")
    print(driver.title)
    search_bar = driver.find_element_by_id("twotabsearchtextbox")
    search_bar.clear()
    search_bar.send_keys(searchname)
    search_bar.send_keys(Keys.RETURN)

    data_dict = dict()

    soup = BeautifulSoup(driver.page_source, 'lxml')
    for div in soup.select('div[data-asin]'):
        if div.select_one('.a-text-normal') is not None:
            print("1st IF")
            if searchname.lower() in div.select_one('.a-text-normal').text.lower():
                print("2nd IF")
                itemName = div.select_one('.a-text-normal').text
                if div.select_one('.a-price') is not None:
                    print("3rd IF")
                    price = div.select_one('.a-price ').get_text('|',strip=True).split('|')[0]
                    image = div.find('img')

                    data_list = []

                    data_list.insert(0, convertprice(price))
                    data_list.insert(1, image['src'])
                    data_dict[itemName] = data_list

                    print(itemName)
                    print(convertprice(price))
                    print(image['src'])
        else:
            continue
    driver.close()
    return data_dict

def convertprice(price):
    price = price.strip("CDN$")
    price = price.lstrip()
    price = price.rstrip(',')
    return Decimal(price)