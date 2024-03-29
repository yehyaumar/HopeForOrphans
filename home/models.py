import uuid
from datetime import datetime, date

from django.db import models
from django.urls import reverse

from HopeForOrphans import settings


# Create your models here.

class Hobby(models.Model):
    name = models.CharField(max_length=64, help_text='Enter a hobby (e.g. cricket, football, gardening)')

    def __str__(self):
        """String for representing the model object"""
        return self.name


class Orphan(models.Model):
    first_name = models.CharField(max_length=64, help_text='First Name')
    last_name = models.CharField(max_length=64, help_text='Last Name')

    dob = models.DateField(help_text='Date of Birth')

    @property
    def calculate_age(self):
        if self.dob:
            return int((datetime.now().year - self.dob.year))

    # age = calculate_age()

    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female')
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICE,
        help_text='Gender',
        default='m',
    )

    orphanage = models.ForeignKey('Orphanage', on_delete=models.CASCADE)

    ADOPTION_STATUS = (
        ('a', 'Available'),
        ('n', 'Not Available'),
        ('u', 'Unknown'),
    )

    status = models.CharField(
        max_length=1,
        choices=ADOPTION_STATUS,
        help_text='Adoption Status',
        default='a'
    )

    date_joined = models.DateField(null=True, blank=True)

    def display_hobbies(self):
        return ', '.join(hobby.name for hobby in self.hobbies.all()[:3])

    hobbies = models.ManyToManyField(Hobby, help_text='Select hobbies', blank=True)

    education = models.CharField(max_length=64, blank=True, help_text='Education')

    avatar = models.ImageField(upload_to='orphans_dp/', null=True, blank=True)

    def __str__(self):
        return '{0} {1}, {2}'.format(self.first_name, self.last_name, self.dob)

    def get_absolute_url(self):
        return reverse('orphan-detail', args=[str(self.id)])

    class Meta:
        ordering = ['first_name', 'last_name']


def uploaded_dir_orphans(instance, filename):
    return 'user_{0}/{1}'.format(instance.orphan.orphanage.user.id, filename)


def uploaded_dir(instance, filename):
    return 'user_{0}/{1}'.format(instance.orphanage.user.id, filename)


class OrphansImages(models.Model):
    image = models.ImageField(upload_to=uploaded_dir_orphans, null=True, blank=True,
                              help_text='Upload an image')

    orphan = models.ForeignKey('Orphan', on_delete=models.CASCADE)


class OrphanagesImages(models.Model):
    image = models.ImageField(upload_to=uploaded_dir, null=True, blank=True,
                              help_text='Upload an image')

    orphanage = models.ForeignKey('Orphanage', on_delete=models.CASCADE)


class BankDetail(models.Model): #PayU Money gateway
    # account_num = models.IntegerField(help_text='16 digit account number')
    # bank_name = models.CharField(max_length=128, help_text='Bank name')
    # ifsc_code = models.CharField(max_length=64, help_text='IFSC code of bank branch')

    merchant_key = models.CharField(max_length=64, help_text='Merchant Key from PayU Money')
    merchant_salt = models.CharField(max_length=64, help_text='Merchant Salt from PayU Money')

    def __str__(self):
        return '{0}: {1}'.format(self.merchant_key, self.merchant_salt)


class Address(models.Model):
    locality = models.CharField(max_length=64, help_text='Locality')
    city = models.CharField(max_length=64, help_text='City')
    state = models.CharField(max_length=64, help_text='State') #choices
    zip_pin_code = models.CharField(max_length=12, help_text='Zip/Pin code')
    country = models.CharField(max_length=64, help_text='Country') #choices

    def __str__(self):
        return str(self.zip_pin_code) + ', ' + self.locality + ', ' + self.city + '\n'\
               + self.state + ', ' + self.country


class Contact(models.Model):

    website = models.URLField(help_text='Associated Website', null=True, blank=True)

    phone_number = models.CharField(max_length=32, help_text='Phone number')
    mobile_number = models.CharField(max_length=32, help_text='Mobile number', null=True, blank=True)

    # fb, insta, twitter

    def __str__(self):
        return '{0}, {1}\n{2}'.format(self.phone_number, self.mobile_number,
                                           self.website)


class IncomeSource(models.Model):
    name = models.CharField(max_length=64, help_text='Enter income source')

    def __str__(self):
        return self.name


class Facilities(models.Model):
    name = models.CharField(max_length=64,
                            help_text="Enter facilities provided")

    def __str__(self):
        return self.name


class Orphanage(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    name = models.CharField(max_length=256, help_text='Name of Orphanage')

    reg_num = models.CharField(max_length=255, help_text='Registration number',unique=True)

    date_estd = models.DateField(null=True, blank=True, help_text='Date of establishment')

    brief_desc = models.TextField(max_length=1024, help_text='Brief description of Orphanage', blank=True)

    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, help_text='Address')
    contact = models.OneToOneField(Contact, on_delete=models.SET_NULL, null=True, help_text='Contact')

    bank_details = models.OneToOneField(BankDetail, on_delete=models.SET_NULL, null=True, blank=True, help_text='Bank details')

    def display_incomesrc(self):
        return ', '.join(income.name for income in self.income_source.all()[:3])

    income_source = models.ManyToManyField(IncomeSource, help_text='Source of Income', blank=True)

    def display_facilities(self):
        return ', '.join(facility.name for facility in self.facilities.all()[:3])

    facilities = models.ManyToManyField(Facilities, help_text='Facilities Available', blank=True)

    display_pic = models.ImageField(upload_to='orphanage_dp/', default='dream_home.gif', help_text='Display picture for orphanage',
                                    null=True, blank=True)

    activated = models.BooleanField('Activated', default=False)

    def __str__(self):
        return '{0}'.format(self.name)

    def get_absolute_url(self):
        return reverse('orphanage-detail', args=[str(self.id)])

    class Meta:
        ordering = ['name', 'date_estd']
    # chairman


class Donor(models.Model):
    first_name = models.CharField(max_length=64, help_text='First Name', blank=True)
    last_name = models.CharField(max_length=64, help_text='Last Name', blank=True)

    date = models.DateTimeField(auto_now_add=True, help_text='Donation date/time')

    phone_number = models.CharField(max_length=32, help_text='Phone number', null=True, blank=True)
    email = models.EmailField(help_text='Email', null=True, blank=True)

    amount_donated = models.FloatField(help_text='Donation Amount')
    payuMoneyId = models.CharField(unique=True, max_length=20, help_text='payu Money ID', null=True)
    donation_remark = models.CharField(max_length=1024, help_text='Donation Remarks', null=True, blank=True)

    donated_to = models.ForeignKey('Orphanage', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name', 'last_name', 'amount_donated']


def generate_urid():
    year = date.today().year
    month = date.today().month
    day = date.today().day

    last_request = AdoptionRequest.objects.all().order_by('request_id').last()
    if not last_request:
        return 'HOP-' + str(year) + str(month).zfill(2) + str(day).zfill(2) + '000000'

    request_id = last_request.request_id
    request_id_number = int(request_id[12:18])
    request_id_day = int(request_id[10:12])
    request_id_month = int(request_id[8:10])
    request_id_year = int(request_id[4:8])

    print(request_id_day, request_id_month, request_id_year)
    if day != request_id_day:
        request_id_number = 0

    new_request_id_number = request_id_number + 1
    new_request_id = 'HOP-' + str(year) + str(month).zfill(2) + str(day).zfill(2) + \
                     str(new_request_id_number).zfill(6)
    return new_request_id


class AdoptionRequest(models.Model):
    first_name = models.CharField(max_length=64, help_text='First Name')
    last_name = models.CharField(max_length=64, help_text='Last Name')

    request_id = models.CharField(primary_key=True, default=generate_urid,editable=False, max_length=18)

    request_date = models.DateTimeField(auto_now_add=True, help_text='Adoption request date/time')

    dob = models.DateField(help_text='Date of Birth (For age purpose)')
    phone_number = models.CharField(max_length=32, help_text='Phone number')
    mobile_number = models.CharField(max_length=32, blank=True)
    email = models.EmailField(help_text='Email', null=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, help_text='Address', null=True)

    occupation = models.CharField(max_length=64, help_text='Occupation')

    income = models.FloatField(help_text='Annual income')

    MARRIAGE_STATUS = (
        ('m', 'Married'),
        ('u', 'Un-married'),
        ('d', 'Divorced'),
    )

    married = models.CharField(
        max_length=1,
        default='m',
        choices=MARRIAGE_STATUS,
        help_text='Marriage Status'
    )

    family_members = models.IntegerField('Total number of family members')

    requested_for = models.ForeignKey(Orphan, on_delete=models.CASCADE)

    CHOICE = (
        ('a', 'Approved'),
        ('d', 'Declined'),
        ('p', 'Pending'),
    )
    approved = models.CharField(max_length=1, default='p', choices=CHOICE)

    class Meta:
        ordering = ['first_name', 'last_name', 'request_id']

