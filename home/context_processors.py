'''
Additional context processor to provide variables to base.html
'''


def navbar_processor(request):
    '''
    Provides the url paths and names to base.html template
    so that active class and aria attritbute can be dynamically
    added
    '''
    navlinks = {
        '/': 'home',
        '/contact/': 'contact',
    }

    return {
        'navlinks': navlinks,
    }
