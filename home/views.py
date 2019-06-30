from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.template.loader import render_to_string

from home.forms import OrphanageSignUpForm, AddressForm, ContactForm, BankDetailForm, OrphanForm, AdoptionApprovalForm
from home.models import Orphanage, IncomeSource, Facilities, Orphan, AdoptionRequest
from users.forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(data=request.POST)
        profile_form = OrphanageSignUpForm(data=request.POST)
        address_form = AddressForm(data=request.POST)
        contact_form = ContactForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() \
                and address_form.is_valid() and contact_form.is_valid():

            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            address = address_form.save()
            contact = contact_form.save()

            user.is_active = False

            user.save()
            profile.user = user

            profile.address = address
            profile.contact = contact

            if 'display_pic' in request.FILES:
                profile.display_pic = request.FILES['display_pic']

            profile.save()
            return render(request, 'registration/wait_for_confirmation.html')
        else:
            print(user_form.errors, profile_form.errors, address_form.errors, contact_form.errors)
    else:
        user_form = CustomUserCreationForm()
        profile_form = OrphanageSignUpForm()
        address_form = AddressForm()
        contact_form = ContactForm()

    return render(request, 'registration/signup.html',
                  {
                      'user_form':user_form,
                      'profile_form':profile_form,
                      'address_form':address_form,
                      'contact_form':contact_form,
                  })


@login_required
def orphanage_profile(request):
    user = request.user

    orphanage = get_object_or_404(Orphanage, user=user)
    donation_list = orphanage.donor_set.all()

    total_donation_raised = 0
    for donor in donation_list:
        total_donation_raised += donor.amount_donated

    return render(request, 'orphanage_profile.html', {
        'orphanage': orphanage,
        'total_donation_raised': total_donation_raised
    })


@login_required
def edit_profile(request):
    user = request.user
    orphanage = get_object_or_404(Orphanage, user=user)

    profile_form = OrphanageSignUpForm(data=request.POST or None, instance=orphanage)
    address_form = AddressForm(data=request.POST or None, instance=orphanage.address)
    contact_form = ContactForm(data=request.POST or None, instance=orphanage.contact)
    bank_details_form = BankDetailForm(data=request.POST or None, instance=orphanage.bank_details)

    if request.method == 'POST':
        if profile_form.is_valid() and address_form.is_valid() \
                and contact_form.is_valid() and bank_details_form.is_valid():

            # user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)

            address = address_form.save()
            contact = contact_form.save()
            bank_details = bank_details_form.save()
            # user.save()
            # profile.user = user
            profile.address = address
            profile.contact = contact
            profile.bank_details = bank_details

            if 'display_pic' in request.FILES:
                profile.display_pic = request.FILES['display_pic']

            profile.save()
            profile_form.save_m2m()
            return redirect('profile')
        else:
            print(profile_form.errors, address_form.errors, contact_form.errors)

    return render(request, 'edit_profile.html',{
        'profile_form': profile_form,
        'address_form': address_form,
        'contact_form': contact_form,
        'bank_details': bank_details_form,
    })


@login_required
def add_orphan(request):
    user = request.user
    orphanage = get_object_or_404(Orphanage, user=user)

    orphan_form = OrphanForm(data=request.POST)
    if request.method == 'POST':
        if orphan_form.is_valid():
            orphan = orphan_form.save(commit=False)
            orphan.orphanage = orphanage
            orphan.save()
            return redirect('my-orphans')
        else:
            print(orphan_form.errors)
    else:
        orphan_form = OrphanForm()

    return render(request, 'add_orphan_form.html', {
        'orphan_form': orphan_form
    })


@login_required
def edit_orphan(request, pk):
    user = request.user
    orphanage = get_object_or_404(Orphanage, user=user)
    # check if the orphan belong to this user

    orphan = get_object_or_404(Orphan, pk=pk)

    if orphan in orphanage.orphan_set.all():
        orphan_form = OrphanForm(data=request.POST or None, instance=orphan)

        if request.method == 'POST':
            if orphan_form.is_valid():
                orphan_form.save()
                return redirect('my-orphans')

            else:
                print(orphan_form.errors)

        return render(request, 'edit_orphan_form.html', {
            'orphan_form': orphan_form
        })
    else:
        return HttpResponse(status=403)


@login_required
def delete_orphan(request):
    user = request.user
    orphanage = get_object_or_404(Orphanage, user=user)

    if request.POST:
        pk = request.POST['pk']
        result = False

        if pk:
            try:
                orphan = orphanage.orphan_set.get(pk=pk)
            except Exception:
                return HttpResponse(status=404)

            result = orphan.delete()

        data = {
            'success': False
        }

        if result:
            data['success'] = True
        else:
            data['success'] = False

        return JsonResponse(data)


@login_required
def my_orphans(request):
    user = request.user

    orphanage = get_object_or_404(Orphanage, user=user)
    orphans = orphanage.orphan_set.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(orphans, 10)
    try:
        orphans = paginator.page(page)
    except PageNotAnInteger:
        orphans = paginator.page(1)
    except EmptyPage:
        orphans = paginator.page(paginator.num_pages)

    return render(request, 'my_orphans_list.html',{
        'orphanage':orphanage,
        'orphans': orphans
    })

# bug
def orphan_detail(request, pk):

    orphan = get_object_or_404(Orphan, pk=pk)

    return render(request, 'orphan_profile.html', {
        'orphan': orphan,
    })


@login_required
def add_income_src(request):
    income_src = request.POST.get('value', None)
    print(income_src)
    # orphanage = Orphanage.objects.get(user=request.user)
    # i_s = orphanage.income_source.create(name=income_src)

    result = IncomeSource.objects.create(name=income_src)
    data = {
        'success': False
    }

    if result:
        data['success'] = True
    else:
        data['success'] = False

    return JsonResponse(data)


@login_required
def add_facility(request):
    facility = request.POST.get('value', None)
    # orphanage = Orphanage.objects.get(user=request.user)
    # fc = orphanage.facilities.create(name=facility)
    result = Facilities.objects.create(name=facility)
    data = {
        'success': False
    }

    if result:
        data['success'] = True
    else:
        data['success'] = False
    return JsonResponse(data)


@login_required
def adoption_requests(request):
    user = request.user
    orphanage = get_object_or_404(Orphanage, user=user)
    orphans = orphanage.orphan_set.all()

    adopt_requests = AdoptionRequest.objects.none()

    for orphan in orphans:
        adopt_requests |= orphan.adoptionrequest_set.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(adopt_requests, 10)
    try:
        adopt_requests = paginator.page(page)
    except PageNotAnInteger:
        adopt_requests = paginator.page(1)
    except EmptyPage:
        adopt_requests = paginator.page(paginator.num_pages)

    return render(request, 'adoption_requests.html', {
        'adopt_requests': adopt_requests
    })


@login_required
def adoption_approval(request):
    data = dict()
    context = dict()
    method = request.method
    request_id = None

    if method == 'GET':
        request_id = request.GET.get('request_id')
    elif method == 'POST':
        request_id = request.POST.get('request_id')

    if request_id:
        adoption_request = AdoptionRequest.objects.get(request_id=request_id)
        adoption_approval_form = AdoptionApprovalForm(request.POST or None, instance=adoption_request)
        if method == 'POST':
            if adoption_approval_form.is_valid():
                adoption_approval_form.save()
                data['form_is_valid'] = True

            else:
                data['form_is_valid'] = False

        context = {
            'adopt_request': adoption_request,
            'adoption_approval_form': adoption_approval_form
        }
    else:
        data['form_is_valid'] = False

    data['html_form'] = render_to_string(template_name='partial_adoption_approval.html', context=context, request=request)

    return JsonResponse(data)


@login_required
def donations(request):
    user = request.user
    orphanage = get_object_or_404(Orphanage, user=user)
    donors_list = orphanage.donor_set.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(donors_list, 10)
    try:
        donors = paginator.page(page)
    except PageNotAnInteger:
        donors = paginator.page(1)
    except EmptyPage:
        donors = paginator.page(paginator.num_pages)

    return render(request, 'donors_list.html', {
        'donors': donors
    })