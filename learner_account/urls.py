from . import views
from django.urls import path

urlpatterns = [
    path('learner_account/', views.AccountPage.as_view(), name='learner_account'),
]