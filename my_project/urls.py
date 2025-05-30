"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import serializers, viewsets, routers
from user.models import CustomUser
from testing import views
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.views.static import serve
# from user.models import User

# Serializer define the API representation
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# # Viewset define the behaviour of Views
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# Router are used for automatic routing


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

def trigger_error(request):
    division_by_zero = 1 / 0


if settings.DEBUG:
    urlpatterns = [
        # path('', include(router.urls)),
        path('admin/', admin.site.urls),
        path('', include('user.urls')),
        path('post/', include('post.urls')),
        path('products/', include('a_stripe.urls'), name="products"),
        # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        # path('postapi/', include('post.api_urls.urls')),
        # path('userapi/', include('user.api_urls.urls')),
        path('sentry-debug/', trigger_error),
        path('api/', include('api_urls.urls')),
        path('sauth/', include('social_django.urls', namespace='social')),
        # path('testing/', cache_page(30)(views.testHome)),
        # path('testing/home/', views.testHome),
        # path('testing/contact/', views.contact),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

else:
    urlpatterns = [
        # path('', include(router.urls)),
        path('admin/', admin.site.urls),
        path('', include('user.urls')),
        path('post/', include('post.urls')),
        path('products/', include('a_stripe.urls'), name="products"),
        # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        # path('postapi/', include('post.api_urls.urls')),
        # path('userapi/', include('user.api_urls.urls')),
        path('sentry-debug/', trigger_error),
        path('api/', include('api_urls.urls')),
        path('sauth/', include('social_django.urls', namespace='social')),
        # path('testing/', cache_page(30)(views.testHome)),
        # path('testing/home/', views.testHome),
        # path('testing/contact/', views.contact),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
