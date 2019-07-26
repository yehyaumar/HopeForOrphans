from MySQLdb._exceptions import IntegrityError
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

import hashlib
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from HopeForOrphans import settings
from .payumoney import PAYU


# Create your views here.
from django.template.loader import render_to_string, get_template

from home.forms import AdoptionRequestForm, AddressForm
from home.models import Orphanage, Orphan,  Donor


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

    donation_list = orphanage.donor_set.all()

    total_donation_raised = 0
    for donor in donation_list:
        total_donation_raised += donor.amount_donated

    return render(request, 'orphanage_profile.html', {
        'orphanage': orphanage,
        'total_donation_raised': total_donation_raised,
    })


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

            template = get_template('emails/adoption_request_email.html')

            email_message = template.render({'orphan_name': adoption_req.requested_for.first_name + ' ' +
                                            adoption_req.requested_for.last_name,
                            'request_id': adoption_req.request_id})
            send_mail('Hope for Orphans - Adoption Request', email_message,
                      recipient_list=[str(adoption_req.email),], from_email=settings.EMAIL_HOST_USER)
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


payu = PAYU()


def donate(request, pk):
    orphanage = get_object_or_404(Orphanage, pk=pk)

    if request.method == 'POST':
        hash_object = hashlib.sha256(b'randint(0,20)')
        txnid = hash_object.hexdigest()[0:20]

        merchant_key = orphanage.bank_details.merchant_key.strip()
        payu_key = orphanage.bank_details.merchant_key.strip()
        payu_salt = orphanage.bank_details.merchant_salt.strip()

        print(payu_key)
        print(payu_salt)

        mode = 'TEST'
        success_url = 'http://127.0.0.1:8000/donate/success'
        failure_url = 'http://127.0.0.1:8000/donate/failure'

        amount = request.POST.get('amount')
        firstname = request.POST.get('firstname')
        email = request.POST.get('email')
        productinfo = request.POST.get('productinfo')
        phone = request.POST.get('phone')
        udf1 = request.POST.get('udf1')
        udf2 = request.POST.get('udf2')

        payment_data = {
            'txnid': txnid,
            'amount': amount,
            'firstname': firstname,
            'email': email,
            'phone': phone,
            'productinfo': productinfo,
            'udf1': udf1,
            'udf2': udf2
        }

        payu_data = payu.initiate_transaction(merchant_key=merchant_key, payu_salt= payu_salt,
                                         payu_key=payu_key, mode=mode, success_url=success_url,
                                         failure_url=failure_url, data=payment_data)
        return JsonResponse(payu_data)

    return render(request, 'checkout.html', {
        'orphanage': orphanage
    })


@csrf_protect
@csrf_exempt
def success(request):
    payu_success_data = payu.check_hash(dict(request.POST))
    amount_donated = payu_success_data['data']['amount']
    pk = int(payu_success_data['data']['udf1'])

    orphanage = get_object_or_404(Orphanage, pk=pk)

    try:
        donation = Donor.objects.create(amount_donated=amount_donated, donated_to=orphanage)
        donation.first_name = payu_success_data['data']['firstname']
        donation.last_name = payu_success_data['data']['lastname']
        donation.email = payu_success_data['data']['email']
        donation.payuMoneyId = payu_success_data['data']['payuMoneyId']
        donation.phone_number = payu_success_data['data']['phone']
        donation.donation_remark = payu_success_data['data']['udf2']

        donation.save()
    except IntegrityError:
        return HttpResponse(status=403)

    return render(request, 'donation_success.html', {
        'success_data': donation
    })


@csrf_protect
@csrf_exempt
def failure(request):
    payu_failure_data = payu.check_hash(dict(request.POST))

    failure_data ={
        'first_name': payu_failure_data['data']['firstname'],
        'amount': payu_failure_data['data']['amount'],
    }

    return render(request, 'donation_failure.html', {
        'failure_data': failure_data
    })