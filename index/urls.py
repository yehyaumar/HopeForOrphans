from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orphanages', views.orphanages_list, name='orphanages'),
    path('orphans', views.orphans_list, name='orphans'),
    path('orphanage/<int:pk>',views.orphanage_view, name='orphanage_view'),
    path('orphanage/<int:pk>/orphans', views.orphanages_orphan_list, name='orphanages_orphan_list'),

]