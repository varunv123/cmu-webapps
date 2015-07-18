from django.conf.urls import patterns, include, url
from django.contrib import admin
from slobbbyApp.forms import *

regform = RegistrationForm()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Team110Proj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'slobbbyApp.views.home'),
    url(r'^get-stream/(?P<id>\d+)$','slobbbyApp.views.get_stream'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'LoginPage.html','extra_context':{'regform':regform}},name='login'),
    url(r'^register$', 'slobbbyApp.views.register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'slobbbyApp.views.confirm_registration', name='confirm'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^profilePage$','slobbbyApp.views.profile'),
    url(r'^add-event$','slobbbyApp.views.add_event'),
    url(r'^add-group$','slobbbyApp.views.add_group'),    
    url(r'^edit$','slobbbyApp.views.editProfile'),
    url(r'^changePassword$','slobbbyApp.views.changePassword'),
    url(r'^changeEmail$','slobbbyApp.views.changeEmail'),
    url(r'^uploadImage$','slobbbyApp.views.upload_image'),
    url(r'^get-image/(?P<id>\d+)/(?P<userid>\d+)$','slobbbyApp.views.get_image'),
    url(r'^invite-user/(?P<eventid>\d+)/(?P<userid>\d+)$','slobbbyApp.views.invite_user'),
    url(r'^groupPage/add-user-to-group/(?P<groupid>\d+)/(?P<userid>\d+)$','slobbbyApp.views.add_user_to_group'),    
    url(r'^search$','slobbbyApp.views.search'),
    url(r'^userProfile/(?P<id>\d+)$','slobbbyApp.views.userProfile'),
    url(r'^groupPage/(?P<id>\d+)$','slobbbyApp.views.groupPage'),
    url(r'^follow/(?P<id>\d+)$','slobbbyApp.views.follow'),
    url(r'^unfollow/(?P<id>\d+)$','slobbbyApp.views.unfollow'),
    url(r'^block-user/(?P<id>\d+)$','slobbbyApp.views.block_user'),
    url(r'^unblock-user/(?P<id>\d+)$','slobbbyApp.views.unblock_user'),
    url(r'^delete-event/(?P<id>\d+)$','slobbbyApp.views.delete_event'),
    url(r'^forgotPassword$', 'slobbbyApp.views.forgot_password'),
    url(r'^resetPassword$', 'slobbbyApp.views.reset_password'),
    url(r'^resetChangePassword/(?P<username>[a-zA-Z0-9_@\+\-]+)$', 'slobbbyApp.views.reset_change_password'),
    url(r'^confirm-reset/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'slobbbyApp.views.confirm_reset', name='confirm_reset'),

)
