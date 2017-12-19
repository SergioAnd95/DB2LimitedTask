from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', login_required(views.MainView.as_view()), name='main'),
]
