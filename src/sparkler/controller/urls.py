from django.conf.urls.defaults import patterns, include, url
# from django.views.generic.simple import direct_to_template
from django.views.generic import DetailView, ListView

from sparkler.controller.models import Device

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'sparkler.controller.views.home', name='home'),
	url(r'^$',
		ListView.as_view(
			queryset=Device.objects.order_by('house'),
			template_name='controller/index.html',
			context_object_name='device_list'),
		name='device_list'),
	url(r'^(?P<pk>\d+)/$',
		DetailView.as_view(
			model=Device,
			template_name='controller/device_detail.html'),
		name='device_detail'),
	# (r'^(?P<houseCode>\w{1})/(?P<unitCode>\d{1})/$', 'sparkler.controller.views.device_detail'),
	# (r'^(?P<houseCode>\w{1})/(?P<unitCode>\d{1})/$', 'sparkler.controller.views.device_detail'),
)
