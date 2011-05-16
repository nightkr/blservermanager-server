from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', "blmanager.views.index"),
	url(r'^(?P<key>(\{){0,1}[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}(\}){0,1})/$', "blmanager.views.details"),
)
