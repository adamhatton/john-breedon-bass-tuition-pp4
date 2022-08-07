from . import views
from django.urls import path

urlpatterns = [
    path('', views.index_page, name='index'),
    path('home/', views.HomePage.as_view(), name='home'),
    path('contact/', views.ContactSection.as_view(), name='contact')
]