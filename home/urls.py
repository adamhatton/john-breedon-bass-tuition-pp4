from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('contact/', views.ContactSection.as_view(), name='contact')
]