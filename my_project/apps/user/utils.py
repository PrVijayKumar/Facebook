from __future__ import unicode_literals
from django.db import IntegrityError
from rest_framework.views import Response, exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the Rest Framework's exception handler to get the standard error response
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError) and not response:
        # breakpoint()
        if 'empty_email' in str(exc):
            response = Response(
                {
                    'message': 'Email cannot be empty.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        elif 'unique_email' in str(exc):
            response = Response(
                {
                    'message': 'Email already exists.'
                }
            )
    return response