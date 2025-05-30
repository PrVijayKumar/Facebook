from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter
# from .views import UserViewSet

router = DefaultRouter()

# router.register('userhapi/', UserViewSet, basename='users')
app_name = "user"

urlpatterns = [
    path('', views.login, name='login-page'),
    path('register/', views.register, name='register'),
    path('fpass/', views.fpassword, name='forgotpass'),
    path('rpass/<int:id>', views.rpassword, name='respass'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    # path('mypost/', views.mypost, name='mypost'),
    path('allposts/', views.all_posts, name='apost'),
    # path('userhapi/', include(router.urls)),
    path('vcode/<int:id>', views.vcode, name='vcode'),
    path('rcode/<int:id>', views.rcode, name='rcode'),
    path('resetpass/<int:id>', views.resetpass, name='resetpass'),

]