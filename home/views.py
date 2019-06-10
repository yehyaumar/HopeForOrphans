from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from datetime import date, datetime


# Create your views here.
from home.forms import OrphanageSignUpForm, AddressForm, ContactForm, BankDetailForm, OrphanForm
from home.models import Address, Orphanage, Contact, BankDetail, IncomeSource, Facilities
from users.forms import CustomUserCreationForm


def index(request):

    return render(request, 'index.html')


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
            return HttpResponse('Wait for the admin to activate your account after proper verification')
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

    orphanage = Orphanage.objects.get(user=user)

    print(orphanage)

    return render(request, 'orphanage_profile.html', {'orphanage': orphanage})


@login_required
def edit_profile(request):
    user = request.user
    orphanage = Orphanage.objects.get(user=user)

    # user_form = CustomUserCreationForm(data=request.POST or None, instance=user)
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
    orphanage = Orphanage.objects.get(user=user)

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
def my_orphans(request):
    user = request.user

    orphanage = Orphanage.objects.get(user=user)
    orphans = orphanage.orphan_set.all()
    return render(request, 'my_orphans_list.html',{
        'orphanage':orphanage,
        'orphans': orphans
    })


def orphan_detail(request, pk):
    user = request.user
    orphanage = Orphanage.objects.get(user=user)
    orphan = orphanage.orphan_set.get(pk=pk)
    total_days = date.today() - orphan.dob

    return render(request, 'orphan_profile.html', {
        'orphan': orphan,
    })


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