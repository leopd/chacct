from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^register2', 'records.views.calculate_register'),
    (r'^register', 'records.views.show_register'),
    (r'^', include(admin.site.urls)),
)
