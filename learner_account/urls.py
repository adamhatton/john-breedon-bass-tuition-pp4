from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('learner_account/', login_required(views.AccountPage.as_view()), name='learner_account'),
]