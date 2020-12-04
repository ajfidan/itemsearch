from django.shortcuts import render

from itemsearchapp.models import Item

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