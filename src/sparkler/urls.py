from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'sparkler.views.home', name='home'),
	# url(r'^sparkler/', include('sparkler.foo.urls')),
	url(r'^c/', include('sparkler.controller.urls')),
	url(r'^api/', include('sparkler.api.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
