from django.contrib import admin
from .models import LearnerProfile, Testimonial


@admin.register(LearnerProfile)
class LearnerProfileAdmin(admin.ModelAdmin):
    '''
    Adds LearnerProfile model into the admin site
    '''

    list_display = (
        'user_name',
        'first_name',
        'last_name',
        'phone',
        'ability',
        'shortened_about',
    )

    @admin.display(description='Username')
    def user_name(self, obj):
        '''
        Gets the username from the User model
        '''
        return obj.user.username

    @admin.display(description='Name')
    def first_name(self, obj):
        '''
        Gets the first name from the User model
        '''
        return obj.user.first_name

    @admin.display(description='Last Name')
    def last_name(self, obj):
        '''
        Gets the username from the User model
        '''
        return obj.user.last_name

    @admin.display(description='About')
    def shortened_about(self, obj):
        '''
        Shortens the about me info for display in admin panel
        '''
        return obj.about[:100]

    # Code taken from user "devwaseem" on
    # https://stackoverflow.com/questions/56944865/how-to-remove-delete-button-from-django-admin-page
    def has_delete_permission(self, request, obj=None):
        '''
        Disable delete button for LearnerProfiles to prevent issues
        with login
        '''
        if (
            f'{LearnerProfile._meta.app_label}/'
            f'{LearnerProfile._meta.model_name}'
            in request.path
        ):
            return False
        return True
    # End of Code taken from user "devwaseem"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    '''
    Adds Testimonial model into the admin site
    '''

    list_display = ('user', 'content', 'created_on', 'updated_on', 'approved')

    # Testimonial model admin actions
    actions = ['approve_testimonials']

    @admin.action(description='Approve testimonial')
    def approve_testimonials(self, request, queryset):
        '''
        Sets message to being complete
        '''
        queryset.update(approved=True)
