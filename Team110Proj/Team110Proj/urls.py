from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Team110Proj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'slobbbyrobbby/',include('slobbbyApp.urls')),
    url(r'',include('slobbbyApp.urls')),
    url(r'^accounts/', include('allauth.urls')),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    # url(r'', include('social_auth.urls')),
)
