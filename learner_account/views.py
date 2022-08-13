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
        return render(
            request,
            'learner_account.html',
            {
                'user_form': UserForm(),
                'learner_profile_form': LearnerProfileForm(),
            }
        )