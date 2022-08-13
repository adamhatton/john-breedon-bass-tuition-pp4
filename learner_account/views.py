from django.shortcuts import render
from django.views import View
from .forms import UserForm, LearnerProfileForm

class AccountPage(View):
    '''
    Renders the learner's account page
    '''
    def get(self, request):
        '''
        Handles GET requests by rendering the account page
        '''
        # Default each form field to be disabled
        user_form = UserForm()
        for field in user_form.fields:
            user_form.fields[field].disabled = True

        learner_profile_form = LearnerProfileForm()
        for field in learner_profile_form.fields:
            learner_profile_form.fields[field].disabled = True

        return render(
            request,
            'learner_account.html',
            {
                'user_form': user_form,
                'learner_profile_form': learner_profile_form,
            }
        )