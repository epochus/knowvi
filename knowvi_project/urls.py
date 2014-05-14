from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'knowvi_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Enables the admin
    url(r'^admin/', include(admin.site.urls)),

    url(r'^knowvi/', include('knowvi.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
            'serve',
            {'document_root' : settings.MEDIA_ROOT}),  )
