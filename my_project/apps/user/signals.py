from django.dispatch import Signal
# from django.contrib.gis.utils import GeoIP



# # function to get ip address of user
# def get_client_ip(request):
# 	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
# 	if x_forwarded_for:
# 		ip = x_forwarded_for.split(',')[0]
# 	else:
# 		ip = request.META.get('ROMOTE_ADDR')
# 	return ip


# Custom Signal
# event when user attempts to login
request_by_user = Signal()


create_dummy_post = Signal()