from django.db import models

DEVICE_STATUS = (
	(10, 'On'),
	(20, 'Off'),
	(100, 'Unknown'),
)

# Create your models here.
class Device(models.Model):
	"""(Device description)"""
	# 256 possibe addresses
	house = models.CharField(blank=True, max_length=1) # A through P
	unit = models.IntegerField(blank=True, null=True) # 1 through 16
	slug = models.SlugField()
	shortDesc = models.CharField(blank=True, max_length=128)
	longDesc = models.TextField(blank=True)
	status = models.CharField(max_length=1, blank=True, null=True, choices=DEVICE_STATUS)
	# img = models.ImageField(upload_to="/dir/path", height_field=, width_field=)
	
	def get_absolute_url(self):
		# return "http://127.0.0.1:8000/c/{houseCode}/{unitCode}/".format(houseCode=self.house, unitCode=self.unit)
		return "http://127.0.0.1:8000/c/{pk}/".format(pk=self.id)
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return u"Device {houseCode}{unitCode}".format(houseCode=self.house, unitCode=self.unit)
