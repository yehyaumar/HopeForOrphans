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

from home.forms import MyAuthForm, MyPasswordResetForm, MySetPasswordForm, MyPasswordChangeForm

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('index.urls')),
    path('home/', include('home.urls')),
    path('signup/', home_views.signup, name='signup'),
    path('login/', home_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        form_class=MyPasswordResetForm,
    ), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        form_class=MySetPasswordForm,
    ),name='password_reset_confirm'
    ),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ),name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        form_class=MyPasswordChangeForm,
    ),name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html',
    ), name='password_change_done'),
]
#
# urlpatterns += [
#     path('', RedirectView.as_view(url='/home/', permanent=True))
# ]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)