from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cntrains.views.home', name='home'),
    url(r'^smsk/', include('lister.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
