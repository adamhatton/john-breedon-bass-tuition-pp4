from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Testimonial
from bookings.models import Booking
from .forms import UserForm, LearnerProfileForm, TestimonialForm


class AccountPage(View):
    '''
    Renders the learner's account page
    '''
    def get(self, request):
        '''
        Handles GET requests by rendering the account page
        '''
        bookings = Booking.objects.filter(user=request.user)
        user_form = UserForm(instance=request.user)
        learner_profile_form = LearnerProfileForm(instance=request.user.learnerprofile)
        
        if Testimonial.objects.filter(user=request.user).exists():
            testimonial_form = TestimonialForm(instance=request.user.testimonial)
            user_has_testimonial = True
            testimonial_approved = Testimonial.objects.get(user=request.user).approved
        else:
            testimonial_form = TestimonialForm()
            user_has_testimonial = False
            testimonial_approved = 'N/A'
        
        return render(
            request,
            'learner_account.html',
            {
                'bookings': bookings,
                'user_form': user_form,
                'learner_profile_form': learner_profile_form,
                'testimonial_form': testimonial_form,
                'user_has_testimonial': user_has_testimonial,
                'testimonial_approved': testimonial_approved,
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

        # If form isn't valid then return form with enabled fields
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
    '''
    Adds testimonial to the database
    '''
    if request.method == 'POST':
        testimonial = TestimonialForm(request.POST)
        testimonial.instance.user = request.user
        if testimonial.is_valid():
            testimonial.save()
            messages.success(request, 'Testimonial has been sent for approval')
            return redirect('/learner_account/')

    return redirect('/learner_account/')

@login_required
def edit_testimonial(request):
    '''
    Updates a testimonial in the database
    '''
    if request.method == 'POST':
        testimonial = get_object_or_404(Testimonial, user=request.user)
        testimonial_form = TestimonialForm(request.POST, instance=testimonial)
        testimonial_form.instance.approved = False

        if testimonial_form.is_valid():
            testimonial.save()
            messages.success(request, 'Testimonial has been sent for approval')
            return redirect('/learner_account/')

    return redirect('/learner_account/')

@login_required
def delete_testimonial(request):
    '''
    Deletes a testimonial from the database
    '''
    testimonial = get_object_or_404(Testimonial, user=request.user)
    testimonial.delete()
    messages.success(request, 'Testimonial successfully deleted')
    return redirect('/learner_account/')