# # Create your views here.
# from django.http import HttpResponse
# import datetime
# 
# def home(request):
# 	now = datetime.datetime.now()
# 	html = "<html><body>It is now %s.</body></html>" % now
# 	return HttpResponse(html)
# 	
# # def device_list(return, houseCode=None):
# # 	"""docstring for device_list"""
# # 	html = "<html><body>Requested Devices in House Code: %s</body></html>" % (houseCode,)
# # 	return HttpResponse(html)
# 	
# def device_detail(request, deviceCode=None, houseCode=None, unitCode=None):
# 	now = datetime.datetime.now()
# 	if deviceCode:
# 		html = "<html><body>Device Code: %s</body></html>" % (deviceCode,)
# 	else:
# 		assert houseCode and unitCode
# 		html = "<html><body>House Code: %s%s</body></html>" % (houseCode, unitCode)
# 	return HttpResponse(html)