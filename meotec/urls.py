from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('meotec.views',
    url(r'^$', 'home', name='home'),
    url(r'^settings/$', 'settings', name='settings'),
    url(r'^manager/(?P<manager_id>\d+)/command/(?P<command>\w+)/run_init/$', 'run_init', name='run_init'),
    url(r'^manager/(?P<manager_id>\d+)/command/(?P<command>\w+)/run/$', 'run', name='run'),
    url(r'^manager/add/$', 'manager_add', name='manager_add'),
    url(r'^manager/(?P<id>\d+)/edit/$', 'manager_edit', name='manager_edit'),
    url(r'^manager/update/$', 'manager_update', name='manager_update'),
    url(r'^node/(?P<id>\d+)/add/(?P<class_path>[\w\.]+)/$', 'node_add', name='node_add'),
    url(r'^node/(?P<id>\d+)/edit/$', 'node_edit', name='node_edit'),
    url(r'^node/(?P<id>\d+)/del/$', 'node_del', name='node_del'),
)
