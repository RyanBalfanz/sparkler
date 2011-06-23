import subprocess
from piston.handler import BaseHandler
from piston.utils import rc

from sparkler.controller.models import Device

class DeviceHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = Device

	def read(self, request, device_id=None, action=None):
		"""
		Returns a single device if `device_id` is given,
		otherwise a subset.
		"""
		base = Device.objects
		
		if device_id:
			d = base.get(pk=device_id)
			device_desc = ' '.join(d.slug.split('-'))
			if action:
				action = action.lower()
				if action == "on":
					cmd = "say turning on {s} lamp".format(s=device_desc).split()
				elif action == "off":
					cmd = "say turning off {s} lamp".format(s=device_desc).split()
				else:
					return rc.BAD_REQUEST
				
			p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
			output = p1.communicate()[0]
			print output
			
			return rc.ALL_OK
		else:
			return rc.BAD_REQUEST
