from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path(
        "learner_account/",
        login_required(views.AccountPage.as_view()),
        name="learner_account",
    ),
    path(
        "learner_account/",
        include(
            [
                path(
                    "add_testimonial/",
                    views.add_testimonial,
                    name="add_testimonial"
                ),
                path(
                    "edit_testimonial/",
                    views.edit_testimonial,
                    name="edit_testimonial"
                ),
                path(
                    "delete_testimonial/",
                    views.delete_testimonial,
                    name="delete_testimonial",
                ),
            ]
        ),
    ),
]
