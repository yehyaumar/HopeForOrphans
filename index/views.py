from django.shortcuts import render

# Create your views here.
from home.models import Orphanage, Orphan


def index(request):
    return render(request, 'index.html')


def orphanages_list(request):

    orphanages = Orphanage.objects.all()

    return render(request, 'orphanages_list.html', {
        'orphanages': orphanages
    })


def orphans_list(request):
    orphans = Orphan.objects.all()

    return render(request, 'orphans_list.html',{
        'orphans': orphans
    })


def orphanage_view(request, pk):

    orphanage = Orphanage.objects.get(pk=pk)

    print(orphanage)

    return render(request, 'orphanage_profile.html', {'orphanage': orphanage})


def orphanages_orphan_list(request, pk):

    orphanage = Orphanage.objects.get(pk=pk)
    orphans = orphanage.orphan_set.all()

    return render(request, 'my_orphans_list.html',{
        'orphanage':orphanage,
        'orphans': orphans
    })