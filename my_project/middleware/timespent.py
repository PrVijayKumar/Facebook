import logging
from django.utils import timezone
# import time
logger = logging.getLogger(__name__)

class TimeSpentMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # start_time = request.META.get('HTTP_X_REQUEST_START', None)
        # if start_time:
        #     try:
        #         start_time = float(start_time)
        #     except ValueError:
        #         start_time = None
        # else:
        #     start_time = None

        # response = self.get_response(request)

        # if start_time is not None:
        #     duration = (response.request_start - start_time) * 1000
        #     logger.info(f"Request to {request.path} took {duration:.2f} ms")
        # else:
        #     logger.info(f"Request to {request.path} did not have a start time header")
        # print("Time of login")
        if request.user.is_authenticated and request.get_full_path() == "/logout/" and request.method == "POST":
            print(f"{request.user}: {timezone.now() - request.user.last_login}")
            diff = timezone.now() - request.user.last_login
            days = diff.days
            hours = diff.seconds // 3600
            minutes = ((diff.seconds) - (hours * 3600)) // 60
            seconds = (diff.seconds) - (hours * 3600) - (minutes * 60)
            logger.info(f"\n ----User with username: {request.user.username} \n\t spent {days} days, {hours} hours, {minutes} minutes, {seconds} seconds \n\t from {request.user.last_login} to {timezone.now()}\n\n")

        response = self.get_response(request)
        return response