from django.conf.urls.defaults import *
from piston.resource import Resource

from sparkler.api.handlers import DeviceHandler

device_handler = Resource(DeviceHandler)

urlpatterns = patterns('',
	url(r'^device/(?P<device_id>\d+)/(?P<action>\w+)/', device_handler, name="api-device-action"),
	# url(r'^device/(?P<device_id>\d+)/', device_handler, name="api-device-detail"),
	url(r'^devices/', device_handler, name="api-device-list"),
)
