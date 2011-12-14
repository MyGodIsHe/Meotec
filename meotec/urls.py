from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('meotec.views',
    url(r'^$', 'home', name='home'),
    url(r'^settings/$', 'settings', name='settings'),
    url(r'^manager/(?P<manager_id>\d+)/command/(?P<command>\w+)/run_init/$', 'run_init', name='run_init'),
    url(r'^manager/(?P<manager_id>\d+)/command/(?P<command>\w+)/run/$', 'run', name='run'),
    url(r'^manager/add/$', 'manager_add', name='manager_add'),
    url(r'^manager/(?P<id>\d+)/edit/$', 'manager_edit', name='manager_edit'),
    url(r'^manager/update/$', 'manager_update', name='manager_update'),
    url(r'^server/add/$', 'server_add', name='server_add'),
    url(r'^server/(?P<id>\d+)/edit/$', 'server_edit', name='server_edit'),
    url(r'^server/(?P<server_id>\d+)/site/add/$', 'site_add', name='site_add'),
    url(r'^server/(?P<server_id>\d+)/site/(?P<id>\d+)/edit/$', 'site_edit', name='site_edit'),
)
