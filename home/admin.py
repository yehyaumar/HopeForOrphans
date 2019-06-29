from django.contrib import admin


# Register your models here.
from home.models import *

# Orphan, Orphanage, Donor, AdoptionRequest, OrphansImages, OrphanagesImages


class OrphanImagesInline(admin.TabularInline):
    model = OrphansImages
    extra = 0


class OrphanageImagesInline(admin.TabularInline):
    model = OrphanagesImages
    extra = 0


@admin.register(Orphan)
class OrphanAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'avatar', 'dob', 'gender', 'status',
                    'orphanage', 'date_joined', 'display_hobbies', 'education')
    inlines = [OrphanImagesInline]


@admin.register(Orphanage)
class OrphanageAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_pic', 'name', 'address', 'contact', 'bank_details',
                    'display_incomesrc', 'display_facilities')
    inlines = [OrphanageImagesInline]


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'payuMoneyId','date', 'email', 'phone_number',
                    'amount_donated', 'donated_to')


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'request_id', 'request_date', 'email', 'phone_number', 'mobile_number',
                    'married', 'family_members', 'requested_for', 'approved')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hobby)
admin.site.register(Facilities)
admin.site.register(BankDetail)
admin.site.register(IncomeSource)