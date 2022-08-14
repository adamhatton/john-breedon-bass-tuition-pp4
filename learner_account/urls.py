from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('learner_account/', login_required(views.AccountPage.as_view()), name='learner_account'),
    path('learner_account/', include([
        path('learner_account/add_testimonial/', views.add_testimonial, name="add_testimonial"),
        path('learner_account/edit_testimonial/', views.add_testimonial, name="edit_testimonial"),
    ])),
]
