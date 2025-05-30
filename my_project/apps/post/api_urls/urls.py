# from post.api_views.views import PostList
# from post.api_views.views import PostList
from django.urls import path, include
from post.api_views import views
from rest_framework.routers import DefaultRouter
from post.models import PostModel
router = DefaultRouter()
router.register('postapi', views.PostModelViewSet, basename='post')
# router.register('postapi', views.PostViewSet, basename='post')
# router.register('postapi', views.PostReadOnlyModelViewSet, basename='post')
# app_name = 'post_api'
urlpatterns = [
    # path('postinfo/', views.LCPostAPI.as_view(), name='pi'),
    # path('postinfo/<int:pk>/', views.PRUDPostAPI.as_view(), name='pu'),
    # path('postlist/', views.PostList.as_view(), name='pl'),
    # path('postcreate/', views.PostCreate.as_view(), name='pc'),
    # path('createpost/', views.create_post, name='cp'),
    # path('postinfo/<int:pk>/', views.PostDetail.as_view(), name='pi'),
    # path('postupdate/<int:pk>/', views.UpdatePost.as_view(), name='pu'),
    # path('deletepost/<int:pk>/', views.DeletePost.as_view(), name='dp'),
    # path('post/', views.CreateListPost.as_view(), name='lcp'),
    # path('post/<int:pk>/', views.RetrieveUpdatePost.as_view(), name='rup'),
    # path('rdpost/<int:pk>/', views.RetrieveDestroyPost.as_view(), name='rdpost'),
    # path('post/', views.ListCreatePost.as_view(), name='lcp'),
    # path('post/<int:pk>/', views.RetrieveUpdateDestroyPost.as_view(), name='rudp'),
    # path('postapi/', PostList.as_view(), name='postlist')
    # path('postapi/', PostList.as_view(), name='postlist'),
    path('', include(router.urls)),

]