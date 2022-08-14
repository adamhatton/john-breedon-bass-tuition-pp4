from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import UserForm, LearnerProfileForm, TestimonialForm


class AccountPage(View):
    '''
    Renders the learner's account page
    '''
    def get(self, request):
        '''
        Handles GET requests by rendering the account page
        '''
        
        user_form = UserForm(instance=request.user)
        learner_profile_form = LearnerProfileForm(instance=request.user.learnerprofile)
        
        try:
            testimonial_form = TestimonialForm(instance=request.user.testimonial)
        except ObjectDoesNotExist:
            testimonial_form = TestimonialForm()
        return render(
            request,
            'learner_account.html',
            {
                'user_form': user_form,
                'learner_profile_form': learner_profile_form,
                'testimonial_form': testimonial_form,
            }
        )

    def post(self, request):
        '''
        Handles POST requests to the account page coming from
        updating the profile
        '''
        user_form = UserForm(request.POST, instance=request.user)
        learner_profile_form = LearnerProfileForm(request.POST, instance=request.user.learnerprofile)

        if user_form.is_valid() and learner_profile_form.is_valid():
            user_form.save()
            learner_profile_form.save()
            messages.success(request, 'Profile successfully updated')
            return redirect('/learner_account/')

        else:
            user_form.helper.layout = user_form.enabled_layout
            learner_profile_form.helper.layout = learner_profile_form.enabled_layout

            return render(
                request,
                'learner_account.html',
                {
                    'user_form': user_form,
                    'learner_profile_form': learner_profile_form,
                }
            )

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        testimonial = TestimonialForm(request.POST)
        testimonial.instance.user = request.user
        if testimonial.is_valid():
            testimonial.save()
            return redirect('/learner_account/')

    return redirect('/learner_account/')