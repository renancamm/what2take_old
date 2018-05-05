from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import BackpackForm
from .models import Backpack, BackpackItem


def backpack_new(request):
    if request.method == "POST":
        form = BackpackForm(request.POST)
        if form.is_valid():
            new_backpack = form.save()
            new_backpack.add_products()
            new_backpack.save()
            return redirect('backpack-detail', id=new_backpack.pk)
    else:
        form = BackpackForm()
    return render(request, 'backpack_new.html', {'form': form})


def backpack_detail(request, id):
    try:
        backpack = Backpack.objects.get(pk=id)
        items = backpack.backpackitem_set.all()
        context = {'backpack': backpack, 'items': items}
    except backpack.DoesNotExist:
        raise Http404("Backpack does not exist")

    return render(request, 'backpack_detail.html', {'context': context})
