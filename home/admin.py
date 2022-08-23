from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    '''
    Adds the Contact model into the admin site
    '''

    list_display = ('name', 'completed', 'shortened_message', 'submitted')
    list_filter = ('submitted', 'completed')
    search_fields = ['name', 'message', 'submitted']

    @admin.display(description='Message')
    def shortened_message(self, obj):
        '''
        Shortens the message for display in admin panel
        '''
        return obj.message[:100]

    # Contact model admin actions
    actions = ['action_message', 'revert_message']

    @admin.action(description='Mark message as actioned')
    def action_message(self, request, queryset):
        '''
        Sets message to being complete
        '''
        queryset.update(completed=True)

    @admin.action(description='Mark message as needing action')
    def revert_message(self, request, queryset):
        '''
        Sets message to needing action
        '''
        queryset.update(completed=False)
