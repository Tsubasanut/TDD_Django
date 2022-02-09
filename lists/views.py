from django.shortcuts import render, redirect
from django.utils.html import escape
from lists.models import Item, List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    filter_list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=filter_list)
            item.full_clean()
            item.save()
            return redirect(filter_list)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': filter_list, 'error': error})


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
    return redirect(list_1)

