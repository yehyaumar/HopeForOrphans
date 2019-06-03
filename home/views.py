from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, datetime


# Create your views here.
from home.forms import OrphanageSignUpForm, AddressForm, ContactForm
from home.models import Address, Orphanage, Contact, BankDetail
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

    user_form = CustomUserCreationForm(data=request.POST or None, instance=user)
    profile_form = OrphanageSignUpForm(data=request.POST or None, instance=orphanage)

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.is_active = False

            user.save()
            profile.user = user
            profile.save()

    return render(request, 'edit_profile.html',{
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def add_orphan(request):
    
    pass


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

