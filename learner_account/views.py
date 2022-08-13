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
        # user_form = UserForm(initial={
        #     'username': request.user.username,
        # })

        user_form = UserForm(instance=request.user)
        return render(
            request,
            'learner_account.html',
            {
                'user_form': user_form,
                'learner_profile_form': LearnerProfileForm(),
            }
        )
