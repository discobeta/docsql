from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
#from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'docsql.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   url(r'^docsql/', include('ds.urls')),

   url(r'^admin/', include(admin.site.urls)),

   (r'^accounts/login/$', 'django.contrib.auth.views.login',
                        {'template_name': 'accounts/login.html'}),

   (r'^oauth2callback', 'ds.views.auth_return'),

   #url(r'^table2sql/$', 'ds.views.table2sql'),

  #  (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'plus/login.html'}),
#
 #   (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'static')

   url(r'^table/(.*)', 'ds.views.table2sql'),

)

