from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^register', 'records.views.show_register'),
    (r'^', include(admin.site.urls)),
)
