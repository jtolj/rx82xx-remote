from schedule_events.models import Schedule_event
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'schedule_events.views.index'),
    url(r'^status.json$', 'schedule_events.views.status'),
    url(r'^events.json$', 'schedule_events.views.events'),
    url(r'^add$', 'schedule_events.views.add'),
    url(r'^(?P<event_id>\d+)/edit$', 'schedule_events.views.edit'),
    url(r'^(?P<event_id>\d+)/delete$', 'schedule_events.views.delete'),
    # url(r'^ericsson_remote/', include('ericsson_remote.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
