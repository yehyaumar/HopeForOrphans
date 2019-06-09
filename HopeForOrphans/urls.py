"""HopeForOrphans URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from HopeForOrphans import settings
from home import views as home_views
from django.contrib.auth import views as auth_views

from home.forms import MyAuthForm

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('home/', include('home.urls')),
    path('signup/', home_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(authentication_form=MyAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ajax/add_income_src', home_views.add_income_src, name='add-income-src'),
    path('ajax/add_facility', home_views.add_facility, name='add-facility'),

]

urlpatterns += [
    path('', RedirectView.as_view(url='/home/', permanent=True))
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)