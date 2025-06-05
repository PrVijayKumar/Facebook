import logging
# import geoip2.database
logger = logging.getLogger(__name__)
from django.contrib.gis.geoip2 import GeoIP2


def get_location(ip):
    g = GeoIP2()
    try:
        location = g.city(ip)
        return {
            'country': location.country.name,
            'city': location.city.name,
            'region': location.region.name
        }
    except Exception:
        return None
class TrackUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # breakpoint()
        if request.get_full_path() == '/' and request.method == 'POST':
        
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # with geoip2.database.Reader('/home/thoughtwin/my_project/my_project/middleware/geoip/') as reader:
            #     result = reader.city(ip)
            #     print(result)
            
            result = get_location(ip)
            if result:
                logger.info(f"IP Address: {ip}, Requested URL: {request.get_full_path()}, Request Method: {request.method}\n Location: {result['city']} {result['country']}")
            else:
                logger.info(f"IP Address: {ip}, Requested URL: {request.get_full_path()}, Request Method: {request.method}")

        response = self.get_response(request)

        return response