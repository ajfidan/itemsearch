from django.shortcuts import render
from itemsearchapp.models import Item

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def index(request):
    return HttpResponseRedirect('/admin/')

def item_search(request):
    item_obj = Item.objects.filter()

    context = {
        "items": item_obj
    }

    return render(request, 'results.html', context)

def searchitem(request):
    if request.method == "POST":
        get_name = request.POST["itemname"]
        get_price = request.POST["itemprice"]





        Item.objects.create(name=get_name, price=get_price)

    
    
    item_obj = Item.objects.filter()

    context = {
        "items": item_obj
    }

    return render(request, 'results.html', context)


def getItemAmazon(searchname):

    headers = { 
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip', 
        'DNT' : '1', # Do Not Track Request Header 
        'Connection' : 'close'
    }

    details = {
        "name": "", "price": ""
    }

    driver = webdriver.Chrome(executable_path=r'\\resources\\chromedriver.exe')
    driver.maximize_window()
    driver.get("https://www.amazon.ca")
    print(driver.title)
    search_bar = driver.find_element_by_id("twotabsearchtextbox")
    search_bar.clear()
    search_bar.send_keys(searchname)
    search_bar.send_keys(Keys.RETURN)

    name = ""
    price = ""
    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for div in soup.select('div[data-asin]'):
            if searchname.lower() in div.select_one('.a-text-normal').text.lower():
                itemName = div.select_one('.a-text-normal').text
                if div.select_one('.a-price'):
                    price = div.select_one('.a-price ').get_text('|',strip=True).split('|')[0]
                    print(itemName)
                    print(ConvertPrice(price))
    except AttributeError:
        pass
    driver.close()
