from django.utils import timezone
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import BackpackForm
from .models import Backpack


def backpack_new(request):
    if request.method == "POST":
        form = BackpackForm(request.POST)
        if form.is_valid():
            backpack = form.save(commit=False)
            backpack.created_at = timezone.now()
            backpack.save()
            return redirect('backpack-detail', id=backpack.pk)
    else:
        form = BackpackForm()
    return render(request, 'backpack_new.html', {'form': form})


def backpack_detail(request, id):
    try:
        backpack = Backpack.objects.get(pk=id)
    except backpack.DoesNotExist:
        raise Http404("Backpack does not exist")

    return render(request, 'backpack_detail.html', {'context': backpack})
