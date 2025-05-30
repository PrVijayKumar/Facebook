from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from api_views import views
from rest_framework.routers import DefaultRouter
from user.auth import CustomAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from post.models import PostModel
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from testing.views import TestingAPI


router = DefaultRouter()

router.register('userapi', views.UserModelViewSet, basename='user')
router.register('postapi', views.PostModelViewSet, basename='post')
router.register('commentapi', views.CommentModelViewSet, basename='comment')
router.register('testapi', views.TestingAPI, basename='test')

# router.register('userapi', views.UserViewSet, basename='user')
# router.register('userapi', views.UserReadOnlyModelViewSet, basename='user')

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
    


]
# print(path('gettoken/', obtain_auth_token))


# from post.api_views.views import PostList
# from post.api_views.views import PostList
