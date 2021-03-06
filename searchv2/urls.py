from django.conf.urls.defaults import patterns, url

from searchv2 import views

urlpatterns = patterns("",

    url(
        regex   = '^build$',
        view    = views.build_search,
        name    = 'build_search',
    ),  
    
    url(
        regex   = '^$',
        view    = views.search,
        name    = 'search',
    ), 
    
    url(
        regex   = '^packages/autocomplete/$',
        view    = views.search_packages_autocomplete,
        name    = 'search_packages_autocomplete',
    ),         

)