from django.shortcuts import render
from itemsearchapp.models import Item
from decimal import Decimal

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib, base64

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
        track_name = request.POST["track_name"].strip()

    print(track_name)
    try:
        item_obj = Item.objects.filter(name__icontains=track_name)
        print(item_obj)
        item_obj.update(isTracked=True)
    except:
        print("Didn't Work")
    else:
        print("It Worked")
    
    context = {
        "items": item_obj,
        "track_name": track_name
    }

    return render(request, 'track.html', context)

def price_history(request):
    
    item_obj = Item.objects.filter(isTracked=True).distinct()
    print(item_obj)

    graphic = ""
    dropdown = ""

    if request.method == "POST":
        dropdown = request.POST["dropdown"].strip()
        print(dropdown)

        selected_obj = Item.objects.filter(name__icontains=dropdown)
        q = selected_obj.values('price', 'created')
        df = pd.DataFrame.from_records(q)

        #Create the scatter chart
        df['price_float'] = df['price'].astype(float).round(2)

        print(df.dtypes)
        df.plot(y='price_float', x='created', color='blue', linestyle='-', marker='o')
        plt.title(dropdown)
        plt.ylabel('$CAD')
        plt.xlabel('Date')

        #Chart to Bytes and convert to context variable
        buf = io.BytesIO()
        plt.savefig(buf, bbox_inches='tight', format='png')
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

    context = {
        "items": item_obj,
        "graphic": graphic
    }

    return render(request, 'pricehistory.html', context)

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
    print(type(searchname))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for div in soup.select('div[data-asin]'):
        if div.select_one('.a-text-normal') is not None:
            print("1st IF")
            listname = searchname.split()
            name = div.select_one('.a-text-normal').text.lower()
            for i, word in enumerate(listname):
                if word.lower() not in name:
                    break
                if (i+1) == len(listname):
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
                if word.lower() in name:
                    continue
            
        else:
            continue
    driver.close()
    return data_dict

def convertprice(price):
    price = price.strip("CDN$")
    price = price.lstrip()
    price = price.rstrip(',')
    return Decimal(price)