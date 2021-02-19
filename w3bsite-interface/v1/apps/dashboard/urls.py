
# imports.
from django.contrib import admin
from django.urls import path
from . import views

# the urls.
urlpatterns = [
    # the .. page.
    path('', views.home.view),
]
