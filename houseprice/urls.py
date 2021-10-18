from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', views.app, name='app'),
    path('result/', views.result, name="result"),
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('search/', views.search, name='search'),
    path('pay/', views.pay, name='pay'),
    path('forms/', views.forms, name='forms'),
]
