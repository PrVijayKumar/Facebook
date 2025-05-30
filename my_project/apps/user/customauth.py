# from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request=None, username=None, password=None, **kwargs):
        # breakpoint()
        username = username
        # breakpoint()
        if not username:
            return None
        
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(email=username)
            except CustomUser.DoesNotExist:
                try:
                    user = CustomUser.objects.get(contact=username)
                except CustomUser.DoesNotExist:
                    # raise AuthenticationFailed('No Such User')
                    return None

        # return (user, None)

        if user.check_password(password):
            return user
        return None


    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except:
            return None
