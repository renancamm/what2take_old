from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import BackpackForm
from .models import Product, Backpack
from django.conf import settings
from datetime import datetime, timedelta
import googlemaps
from darksky import forecast


def backpack_new(request):
    if request.method == "POST":
        form = BackpackForm(request.POST)
        if form.is_valid():
            new_backpack = form.save()

            #Request geocode and weather forecast
            gmaps = googlemaps.Client(key=settings.GOOGLEMAPS_KEY)
            geocode_result = gmaps.geocode(request.POST['place'])
            geocode_lat = geocode_result[0]['geometry']['location']['lat']
            geocode_lng = geocode_result[0]['geometry']['location']['lng']
            forecast_result = forecast(settings.DARKSKY_KEY, geocode_lat, geocode_lng, units='si')
            forecast_temp = forecast_result.temperature
            #Set temperarture
            new_backpack.temp = forecast_temp

            #Calculate time delta
            delta_start = datetime.strptime(request.POST['start_date'], "%m/%d/%Y").date()
            delta_end = datetime.strptime(request.POST['end_date'], "%m/%d/%Y").date()
            delta = (delta_end - delta_start).days
            #Set days
            new_backpack.days = delta

            #Set produt list
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
