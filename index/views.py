from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string

from home.forms import AdoptionRequestForm, AddressForm, AdoptionApprovalForm
from home.models import Orphanage, Orphan, AdoptionRequest


def index(request):
    return render(request, 'index.html')


def orphanages_list(request):
    orphanages = Orphanage.objects.all()

    return render(request, 'orphanages_list.html', {
        'orphanages': orphanages
    })


def orphans_list(request):
    orphans = Orphan.objects.all()

    return render(request, 'orphans_list.html', {
        'orphans': orphans
    })


def orphanage_view(request, pk):
    orphanage = Orphanage.objects.get(pk=pk)

    print(orphanage)

    return render(request, 'orphanage_profile.html', {'orphanage': orphanage})


def orphanages_orphan_list(request, pk):
    orphanage = Orphanage.objects.get(pk=pk)
    orphans = orphanage.orphan_set.all()

    return render(request, 'my_orphans_list.html', {
        'orphanage': orphanage,
        'orphans': orphans
    })


def adoption_request(request):
    data = dict()

    if request.method == 'POST':
        adopt_req_form = AdoptionRequestForm(request.POST)
        address_form = AddressForm(request.POST)

        if address_form.is_valid() and address_form.is_valid():
            pk = request.POST.get('pk')
            orphan = Orphan.objects.get(pk=pk)

            adoption_req = adopt_req_form.save(commit=False)
            address = address_form.save()
            adoption_req.address = address
            adoption_req.requested_for = orphan
            adoption_req.save()
            data['form_is_valid'] = True
            data['success_page'] = render_to_string(template_name='partial_success_adopt_req.html')

        else:
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


