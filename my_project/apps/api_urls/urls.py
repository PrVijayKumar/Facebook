from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include, get_resolver
from api_views import views
from rest_framework.routers import DefaultRouter
from user.auth import CustomAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from post.models import PostModel
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
# from testing.views import TestingAPI

# testing code start
# from rest_framework.schemas import get_schema_view
# from rest_framework.renderers import JSONOpenAPIRenderer


# schema_view = get_schema_view(
#     title="Server Monitoring API",
#     url="https://www.example.org/api/",
#     renderer_classes=[JSONOpenAPIRenderer],
# )
# testing code end




router = DefaultRouter()

router.register('userapi', views.UserModelViewSet, basename='user')
router.register('postapi', views.PostModelViewSet, basename='post')
router.register('commentapi', views.CommentModelViewSet, basename='comment')
router.register('testapi', views.TestingAPI, basename='test')

# router.register('userapi', views.UserViewSet, basename='user')
# router.register('userapi', views.UserReadOnlyModelViewSet, basename='user')


# Custom API Root
class CustomAPIRoot(APIView):
    def get(self, request, format=None):
        # endpoints = set(v[1] for k,v in get_resolver(None).reverse_dict.items())
        # endpoints = set(str(v[0].pattern_route) for k,v in get_resolver(None).reverse_dict.items() if hasattr(v[0], 'pattern') and hasattr(v[0].pattern, '_route'))
        # resolver = get_resolver()

        # endpoints = set()
        # for key, val_list in resolver.reverse_dict.items():

        #     if not isinstance(key, str):  # Skip non-view-name entries
        #         continue
        #     for val in val_list:
        #         breakpoint()
                # if hasattr(val[0], 'pattern') and hasattr(val[0].pattern, '_route'):
                #     route = val[0].pattern._route
                #     endpoints.add(route)
        resolver = get_resolver()
        pairs = {}
        endpoints = []
        def walk(patterns, prefix=''):
            for pattern in patterns:
                if hasattr(pattern, 'url_patterns'):
                    walk(pattern.url_patterns, prefix + str(pattern.pattern))
                else:
                    route = prefix + str(pattern.pattern)
                    route = route.lstrip('^').rstrip('$')
                    if 'api' in route:
                        route = route.replace('^', "")
                        if "<pk>" not in str(route) and "<format>" not in str(route):
                            endpoints.append(route)
        walk(resolver.url_patterns)
        # walk(router.urls)
        # for pattern in router.urls:
        #     route = str(pattern.pattern)
        #     route = 'api/'+route.lstrip('^').rstrip('$')
        #     if 'P' not in route:
        #         endpoints.append(route)
        # breakpoint()
        for e in endpoints:
            # breakpoint()
            if e != 'api/' and 'drf' not in str(e) and 'auth' not in str(e):
                name = e.strip('/')
                name = name.split('/')[-1]
                # pairs[name] = request.build_absolute_uri(e)
                pairs[name] = f"{request.scheme}://{request.get_host()}/{e}"
        return Response(pairs)



schema_view = get_schema_view(
    openapi.Info(
        title="FBClone API Docs",
        default_version='v1',
        description="Facebook User Register",
        terms_of_service="https://www.google.com/policies/terms",
        contact=openapi.Contact(email="vijaychoudhary@thoughtwin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# app_name = 'user_api'
urlpatterns = [
    # path("user/", views.LCUserAPI.as_view(), name='lcu'),
    # path("user/<int:pk>", views.PRUDUserAPI.as_view(), name='puser'),
    # path("user/", views.UserList.as_view(), name="ul"),
    # path("createuser/", views.CreateUser.as_view(), name="cu"),
    # path("userdetail/<int:pk>/", views.UserDetail.as_view(), name="ud"),
    # path("updateuser/<int:pk>/", views.UpdateUser.as_view(), name="uu"),
    # path("deleteuser/<int:pk>/", views.DeleteUser.as_view(), name="du"),
    # path('user/', views.ListCreateUser.as_view(), name='lcu'),
    # path('user/<int:pk>/', views.RetrieveUpdateUser.as_view(), name='ru'),
    # path('rduser/<int:pk>/', views.RetrieveDestroyUser.as_view(), name='rdu'),
    # path('user/', views.ListCreateUser.as_view(), name='lcu'),
    # path('user/<int:pk>/', views.RetrieveUpdateDestroyUser.as_view(), name='rdup'),
    # path('gettoken/', obtain_auth_token),
    # path('gettoken/', CustomAuthToken.as_view()),
    path('', CustomAPIRoot.as_view(), name='api-root'),
    path('', include(router.urls)),
    # path('testapi/', views.TestingAPI.as_view(), name='test'),
    path('register/', views.RegisterAPI.as_view(), name='create_apiuser'),
    path('login/', views.LoginAPI.as_view(), name='login_apiuser'),
    path('logout/', views.LogoutAPI.as_view(), name='logout_apiuser'),
    path('auth/', include('rest_framework.urls', namespace="rest_framework2")),
    path('gettoken/', TokenObtainPairView.as_view(), name="token_obtain"),
    path('refreshtoken/', TokenRefreshView.as_view(), name="token_refresh"),
    path('verifytoken/', TokenVerifyView.as_view(), name='refresh_token'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('postapi/', include(router.urls)),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path("schema.json", schema_view),
]
# print(path('gettoken/', obtain_auth_token))


# from post.api_views.views import PostList
# from post.api_views.views import PostList

