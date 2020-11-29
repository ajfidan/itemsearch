from django.shortcuts import render

from itemsearchapp.models import Item

def item_search(request):
    item_obj = Item.objects.filter()

    context = {
        "items": item_obj
    }

    return render(request, 'results.html', context)

#def store_item(request):
