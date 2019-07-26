from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orphanages', views.orphanages_list, name='orphanages'),
    path('orphans', views.orphans_list, name='orphans'),
    path('orphanage/<int:pk>',views.orphanage_view, name='orphanage_view'),
    path('orphanage/<int:pk>/orphans', views.orphanages_orphan_list, name='orphanages_orphan_list'),
    path('ajax/adopt_request', views.adoption_request, name='adopt-request'),
    path('donate/<int:pk>', views.donate, name='donate'),
    path('donate/success', views.success, name='donate-success'),
    path('donate/failure', views.failure, name='donate-failure'),
    path('about-us', views.about_us, name='about-us'),
    path('contact-us', views.contact_us, name='contact-us')

]