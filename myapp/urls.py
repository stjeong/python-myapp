"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from myapp.views import RegistrationView
from myapp.views import SessionTestView

urlpatterns = [
    path('bbs/', include('bbs.urls', namespace='bbs')),
    path('admin/', admin.site.urls),
    # url(r'^accounts/', include('django.contrib.auth.urls'))
    path('accounts/', include('django.contrib.auth.urls')),
    # url(r'^accounts/registration', RegistrationView.as_view(), name='registration'),
    path('accounts/registration', RegistrationView.as_view(), name='registration'),

    path('session/', SessionTestView.as_view(), name='session')
]
