from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.orphanage_profile,name='profile'),
    path('my-orphans', views.my_orphans, name='my-orphans'),
    path('add-orphan', views.add_orphan, name='add-orphan'),
    path('orphan/<int:pk>', views.orphan_detail, name='orphan-detail'),
    path('edit-profile', views.edit_profile, name='edit-profile'),

    path('ajax/add_income_src', views.add_income_src, name='add-income-src'),
    path('ajax/add_facility', views.add_facility, name='add-facility'),
    path('ajax/delete-orphan', views.delete_orphan, name='delete-orphan'),

    path('edit-orphan/<int:pk>', views.edit_orphan, name='edit-orphan'),
    path('adoption-requests', views.adoption_requests, name='adoption-requests'),

    path('ajax/adoption_approval', views.adoption_approval, name='adopt-approval')

]