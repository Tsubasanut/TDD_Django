from django.shortcuts import render, redirect
from django.utils.html import escape
from lists.models import Item, List
from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    filter_list = List.objects.get(id=list_id)
    #items = Item.objects.filter(list=filter_list)
    return render(request, 'list.html', {'list': filter_list})

def new_list(request):
    list_1 = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_1)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_1.delete()
        error = escape("You can't have an empty list item")
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{list_1.id}/')

def add_item(request, list_id):
    list_1 = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_1)
    return redirect(f'/lists/{list_1.id}/')
