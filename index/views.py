from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string

from home.forms import AdoptionRequestForm, AddressForm, AdoptionApprovalForm
from home.models import Orphanage, Orphan, AdoptionRequest


def index(request):
    return render(request, 'index.html')


def orphanages_list(request):
    orphanages = Orphanage.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(orphanages, 10)
    try:
        orphanages = paginator.page(page)
    except PageNotAnInteger:
        orphanages = paginator.page(1)
    except EmptyPage:
        orphanages = paginator.page(paginator.num_pages)

    return render(request, 'orphanages_list.html', {
        'orphanages': orphanages
    })


def orphans_list(request):
    orphans = Orphan.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(orphans, 10)
    try:
        orphans = paginator.page(page)
    except PageNotAnInteger:
        orphans = paginator.page(1)
    except EmptyPage:
        orphans = paginator.page(paginator.num_pages)

    return render(request, 'orphans_list.html', {
        'orphans': orphans
    })


def orphanage_view(request, pk):
    orphanage = get_object_or_404(Orphanage, pk=pk)

    return render(request, 'orphanage_profile.html', {'orphanage': orphanage})


def orphanages_orphan_list(request, pk):
    orphanage = get_object_or_404(Orphanage, pk=pk)
    orphans = orphanage.orphan_set.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(orphans, 10)
    try:
        orphans = paginator.page(page)
    except PageNotAnInteger:
        orphans = paginator.page(1)
    except EmptyPage:
        orphans = paginator.page(paginator.num_pages)

    return render(request, 'my_orphans_list.html', {
        'orphanage': orphanage,
        'orphans': orphans
    })


def adoption_request(request):
    data = dict()

    if request.method == 'POST':
        adopt_req_form = AdoptionRequestForm(request.POST)
        address_form = AddressForm(request.POST)

        if adopt_req_form.is_valid() and address_form.is_valid():
            pk = request.POST.get('pk')
            orphan = get_object_or_404(Orphan, pk=pk)

            adoption_req = adopt_req_form.save(commit=False)
            address = address_form.save()
            adoption_req.address = address
            adoption_req.requested_for = orphan
            adoption_req.save()
            data['form_is_valid'] = True
            data['req_id'] = adoption_req.request_id
            data['success_page'] = render_to_string(template_name='partial_success_adopt_req.html')
        else:
            print(adopt_req_form.errors, address_form.errors)
            data['form_is_valid'] = False
    else:
        adopt_req_form = AdoptionRequestForm()
        address_form = AddressForm()

    context = {
        'form': adopt_req_form,
        'address_from': address_form
    }

    data['html_form'] = render_to_string(template_name='partial_adoption_request_form.html',
                                         context=context,
                                         request=request,
                                         )

    return JsonResponse(data)


