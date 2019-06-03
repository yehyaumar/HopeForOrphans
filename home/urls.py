from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.orphanage_profile,name='profile'),
    path('my-orphans', views.my_orphans, name='my-orphans'),
    path('add-orphan', views.add_orphan, name='add-orphan'),
    path('orphan/<int:pk>', views.orphan_detail, name='orphan-detail'),
    path('edit-profile', views.edit_profile, name='edit-profile'),

]