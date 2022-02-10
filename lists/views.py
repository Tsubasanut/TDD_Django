from django.shortcuts import render, redirect
from django.utils.html import escape
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    '''filter_list = List.objects.get(id=list_id)
    error = None
    form = ItemForm()

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['text'], list=filter_list)
            item.full_clean()
            item.save()
            return redirect(filter_list)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': filter_list, 'error': error, 'form': form})'''
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def new_list(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        list_1 = List.objects.create()
        item = Item.objects.create(text=request.POST['text'], list=list_1)
        return redirect(list_1)
    else:
        return render(request, 'home.html', {'form': form })


