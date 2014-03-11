from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'knowvi_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Enables the admin
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^rango/', include('rango.urls')),
)
