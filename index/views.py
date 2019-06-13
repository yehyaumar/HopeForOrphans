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


