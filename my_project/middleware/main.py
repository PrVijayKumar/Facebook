import logging
import time

logger = logging.getLogger(__name__)

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        start_time = time.time()


        # Log request method and path
        method = request.method
        path = request.get_full_path()

        logger.warning(f"Incoming request: method: {method}, path: {path}")

        if method in ['POST', 'PUT', 'PATCH']:
            try:
                body = request.body.decode('utf-8')
                logger.info(f"Request body: {body}")
            except Exception:
                logger.info(f"Failed to decode request body.")


        response = self.get_response(request)

        duration = time.time() - start_time
        logger.warning(f"Response status: {response.status_code} for {method} {path} took {duration:.2f} seconds")
        # user_agent = request.META.get('HTTP_USER_AGENT')

        # print("###")
        # print(user_agent)
        # print(logger)
        # print("###")
        return response