from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import BackpackForm
from .models import Product, Backpack


def backpack_new(request):
    if request.method == "POST":
        form = BackpackForm(request.POST)
        if form.is_valid():
            new_backpack = form.save()
            new_backpack.add_products()
            new_backpack.save()
            return redirect('backpack-detail', backpack_uuid=new_backpack.uuid)
    else:
        form = BackpackForm()
    return render(request, 'backpack_new.html', {'form': form})


def backpack_detail(request, backpack_uuid):
    try:
        backpack = Backpack.objects.get(uuid=backpack_uuid)
        items = backpack.backpackitem_set.all()

        # Build category list
        categories = []
        for item in items:
            if item.product.category not in categories:
                categories.append(item.product.category)

        # Sorte categories based on 'order' property
        categories.sort(key=lambda x: x.order)

        context = {'backpack': backpack, 'items': items, 'categories': categories}

    except backpack.DoesNotExist:
        raise Http404("Backpack does not exist")

    return render(request, 'backpack_detail.html', {'context': context})


def product_detail(request, backpack_uuid, product_id):
    try:
        backpack = Backpack.objects.get(uuid=backpack_uuid)
        product = Product.objects.get(pk=product_id)
        context = {'backpack': backpack, 'product': product}
    except backpack.DoesNotExist:
        raise Http404("Backpack does not exist")
    except product.DoesNotExist:
        raise Http404("Product does not exist")

    return render(request, 'product_detail.html', {'context': context})
