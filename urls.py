from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^register', 'records.views.calculate_register'),
    (r'^', include(admin.site.urls)),
)
