'''
Additional context processor to provide variables to base.html
'''


def navbar_scrollspy_processor(request):
    '''
    Provides the url paths and names to base.html template
    so that active, aria attribute and scrollspy can be dynamically
    added
    '''
    navlinks = {
        '/home/': 'home',
        '/contact/': 'contact',
    }

    return {
        'navlinks_scrollspy': navlinks,
    }


def navbar_processor(request):
    '''
    Provides the url paths and names to base.html template
    for links that need active and aria attribute but not scrollspy
    '''
    navlinks = {
        '/about/': 'about',
    }

    return {
        'navlinks': navlinks,
    }
