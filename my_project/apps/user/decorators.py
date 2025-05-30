# from functools import wraps
# from django.views.decorators.cache import cache_page
# # from django.utils.decorators import available_attrs
# from functools import WRAPPER_ASSIGNMENTS


# def cache_on_auth(timeout):
#     def decorator(view_func):
#         @wraps(view_func, assigned=WRAPPER_ASSIGNMENTS)
#         def _wrapped_view(request, *args, **kwargs):
#             return cache_page(timeout, key_prefix="_auth_%s_" % request.user.is_authenticated())(view_func)(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator