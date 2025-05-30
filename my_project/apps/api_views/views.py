# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# import io
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
# from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView

# from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
# from user.models import User
# from user.serializers import UserSerializer
# from .serializers import PostHyperlinkedSerializer
# from user.api_views.serializers import UserHyperlinkedSerializer
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# import io
# from django.views.decorators.csrf import csrf_exempt
# from django.views import View
# from django.utils.decorators import method_decorator
# import pdb
# from user.models import User
from post.models import PostModel
from user.models import CustomUser

from post.serializers import PostSerializer
from django.views.decorators.csrf import csrf_exempt
import pdb

from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoObjectPermissions, BasePermission
from user.customauth import CustomAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from user.mypaginations import MyPageNumberPagination, MyCursorPagination
from rest_framework.pagination import LimitOffsetPagination, CursorPagination
from django.urls import reverse
from post import urls
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
import logging
from rest_framework import permissions
from post.models import PostModel
from post.serializers import PostSerializer
from django.views.decorators.csrf import csrf_exempt
from user.forms import UserCreationForm
from user.serializers import UserSerializer, UserRegisterSerializer
from rest_framework.authtoken.models import Token

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.db.models.signals import post_save
# from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
# from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
# from rest_framework.response import Response
from django.dispatch import receiver
from django.conf import settings
from user.throttling import JackRateThrottle
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
import logging
from testing.models import DemoTable
from testing.serializers import TestingSerializer
from django.utils import timezone
# from .custompermission import MyPermission


# swagger imports
# from rest_framework.generics import GenericAPIView


# class API(GenericAPIView):

#     serializer_class = UserSerializer
#     def get(self, request):
#         objects = CustomUser.objects.all()
#         serializer = UserSerializer(object, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         # logger for creation of new user
#         logger.info(f"New user with username:{user.username} created successfully at {timezone.now()} with API")
#         return Response({
#             'user': UserSerializer(user, context=self.get_serializer_context()).data,
#         }, status=status.HTTP_201_CREATED)

class TestingAPI(viewsets.ModelViewSet):
    queryset = DemoTable.objects.all()
    serializer_class = TestingSerializer
    # authentication_classes = [JWTAuthentication]
    authentication_classes = []
    permission_classes = []
    # filter_backends = [SearchFilter]
    # search_fields = ['post_title']
    # pagination_class = MyPageNumberPagination
    pagination_class = LimitOffsetPagination


# class TestingAPI(APIView):
#     def get(self, request, pk=None, format=None):
#         id = pk
#         if id is not None:
#             post = DemoTable.objects.get(id=id)
#             serializer = TestingSerializer(post)
#             return Response(serializer.data)
#         posts = DemoTable.objects.all()
#         serializer = TestingSerializer(posts, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = TestingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def put(self, request, pk, format=None):
#         id = pk
#         post = DemoTable.objects.get(id=id)
#         serializer = TestingSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Updated !!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, pk, format=None):
#         id = pk
#         post = DemoTable.objects.get(id=id)
#         serializer = TestingSerializer(post, data=request.data, partial=True)
#         pdb.set_trace()
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Updated Partially !!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         id = pk
#         post = DemoTable.objects.get(id=id)
#         post.delete()
#         return Response({'msg': 'Post Deleted !!'})


logger = logging.getLogger(__name__)


class PostModelPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
        # if request.method == 'GET':
        #     return request.user.is_authenticated
        # elif request.method == 'POST':
        #     # breakpoint()
        #     # logger for new post creation
        #     logger.info(f"{request.user.username} create a new post at {timezone.now()}")
        #     return request.user.is_authenticated
  
    def has_object_permission(self, request, view, obj):
        # breakpoint()
        # return True
        if request.method in permissions.SAFE_METHODS:
            return True  # need to modify so can see own stuff
            # return request.user.id == obj.post_user.id or True  # need to modify so can see own stuff
    #     # breakpoint()
    #     return True
        elif request.method == 'PATCH':
            # breakpoint()
            return request.user.id == obj.post_user.id or request.user.is_staff
        elif request.method == 'DELETE':
            # logger for deleting post
            logger.info(f"{request.user.username} deleted the post with title: {obj.post_title} at {timezone.now()}")
            # return request.user == obj.owner
            return request.user.id == obj.post_user.id or request.user.is_staff
        elif request.method == 'PUT':
            # logger for updating posts
            logger.info(f"{request.user.username} successfully updated the post at {timezone.now()}")
            return request.user.id == obj.post_user.id or request.user.is_staff
        return request.user.id == obj.post_user.id  # need to modify so can see own stuff
    # pass


class PostModelViewSet(viewsets.ModelViewSet):
    # http_method_names = ['get', 'post', 'patch', 'put', 'delete']
    # queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    # authentication_classes = [JWTAuthentication]
    authentication_classes = [SessionAuthentication]
    permission_classes = [PostModelPermissions]
    filter_backends = [SearchFilter]
    search_fields = ['post_title']
    pagination_class = MyPageNumberPagination
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            posts = PostModel.objects.all()
        else:
            posts = PostModel.objects.all()
            # posts = PostModel.objects.filter(post_user_id=self.request.user.id)
        return posts


# @csrf_exempt
# def create_post(request):
#     if request.method == 'POST':
#         breakpoint()
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         # parse the json data to python native data type
#         pythondata = JSONParser().parse(stream)

#         # Now convert native data type to complex data type using serializer class
#         serializer = CreatePostSerializer(data=pythondata)
#         # Now check if incoming data is valid
#         if serializer.is_valid():
#             serializer.save()
#             # logger for post creation
#             logger.info(f"{request.user.username} created a new post with title: {pythondata.post_title} at {timezone.now()}")
#             res = {'msg': 'Post Created'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type="application/json")
#         return JsonResponse(serializer.errors, safe=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


logger = logging.getLogger(__name__)


class UserPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_staff
        elif request.method == 'GET':
            return request.user.is_authenticated


class UserModelViewSet(viewsets.ModelViewSet):
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [JWTAuthentication]
    authentication_classes = [SessionAuthentication]
    permission_classes = [UserPermissions]
    filter_backends = [SearchFilter]
    search_fields = ['username']
    throttle_classes = [AnonRateThrottle]
    pagination_class = MyCursorPagination

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)


class RegisterAPI(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # breakpoint()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # logger for creation of new user
        logger.info(f"New user with username:{user.username} created successfully at {timezone.now()} with API")
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)
    
class LoginAPI(GenericAPIView):
    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # pdb.set_trace()
        try:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'user': UserSerializer(user, context=self.get_serializer_context()).data
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'result': 'Username or Password does not match'
            }, status=status.HTTP_401_UNAUTHORIZED)
        # return super(LoginAPI, self).post(request)


class LogoutAPI(GenericAPIView):
    serializer_class = AuthTokenSerializer
    permission_class = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        try:
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# class UserModelPermissions(DjangoObjectPermissions):
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
#         'HEAD': ['%(app_label)s.view_%(model_name)s'],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }

    # logger.info('in UserModelPermissions')
    # # permissions.SAFE_METHODS = ('GET', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS')
    # def has_permission(self, request, view):
    #     if request.method == 'GET':
    #         breakpoint()
    #         return True
    #     elif request.method == 'POST':
    #         return request.user.is_staff

    # def has_object_permission(self, request, view, obj):
    #     breakpoint()
    #     logger.info('in UserModelPermissions has_object_permission')
    #     print('permissions.SAFE_METHODS: ', permissions.SAFE_METHODS)
    #     if request.method in permissions.SAFE_METHODS:
    #         # return request.user == obj.owner or True # need to modify so can see own stuff
    #         # breakpoint()
    #         return request.user.id == obj.id or True  # need to modify so can see own stuff
    #     elif request.method == 'PATCH':
    #         # breakpoint()
    #         # return request.user == obj.owner
    #         return request.user.id == obj.id or request.user.is_staff
    #     elif request.method == 'DELETE':
    #         # return request.user == obj.owner
    #         return request.user.id == obj.id or request.user.is_staff
    #     elif request.method == 'PUT':
    #         return request.user.id == obj.id or request.user.is_staff
    #     return False
    #     # return request.user.id == obj.id

# class UserModelViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     # serializer_class = UserSerializer
#     serializer_class = UserHyperlinkedSerializer
#     pagination_class = MyCursorPagination
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # filter_backends = [OrderingFilter]
    # ordering_fields = ['username', 'email']
    # search_fields = ['username']
    # pagination_class = MyPageNumberPagination

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['username', 'email']
    # throttle_classes = [AnonRateThrottle, JackRateThrottle]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'userscope'

    # def get_queryset(self):
    #     user = self.request.user
    #     return User.objects.filter(pk=user.id)




# class UserModelViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    # authentication_classes = [SessionAuthentication]
    # authentication_classes = [TokenAuthentication]
    # authentication_classes = [CustomAuthentication]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    # permission_classes = [MyPermission]








# class UserModelViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAdminUser]


# class UserReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



# class UserViewSet(viewsets.ViewSet):
#     def list(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         print("**********list**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         id = pk
#         print("**********retrieve**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if id is not None:
#             user = User.objects.get(pk=id)
#             serializer = UserSerializer(user)
#             return Response(serializer.data)
        
#     def create(self, request):
#         serializer = UserSerializer(data=request.data)
#         print("**********create**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'User Created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def update(self, request, pk):
#         user = User.objects.get(pk=pk)
#         serializer = UserSerializer(user, data=request.data)
#         print("**********update**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'User Updated'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def partial_update(self, request, pk):
#         user = User.objects.get(pk=pk)
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         print("**********partial update**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'User Update Partially'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk):
#         user = User.objects.get(pk=pk)
#         print("**********destroy**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         user.delete()
#         return Response({'msg': 'User Deleted!!'})









# class ListCreateUser(ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class RetrieveUpdateDestroyUser(RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class ListCreateUser(ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class RetrieveUpdateUser(RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class RetrieveDestroyUser(RetrieveDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



# class UserList(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class CreateUser(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UpdateUser(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class DeleteUser(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer




"""class UserAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        id = pk
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User Updated !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id = pk
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User updated partially !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        id = pk
        user = User.objects.get(id=id)
        user.delete()
        return Response({'msg': 'User Deleted !!'})"""



"""@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def UserAPI(request, pk=None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        users = User.objects.all()
        pdb.set_trace()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User Created!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    if request.method == 'PUT':
        id = pk
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User Updated !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PATCH':
        id = pk
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User Updated Partially'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        id = pk
        user = User.objects.get(id=id)
        user.delete()
        return Response({'msg': 'User Deleted!!'})"""

# @decorators(name='patch')
"""@method_decorator(csrf_exempt, name='dispatch')
class UserAPI(View):
    def get(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        pdb.set_trace()
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = UserSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'User Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(serializer.errors, safe=False)
    
    def put(self, request, *args, **kwargs):
        pdb.set_trace()
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=pythondata, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'User Updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(serializer.errors, safe=False)
    
    def delete(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        user = User.objects.get(id=id)
        user.delete()
        res = {'msg': 'User Deleted!!'}
        return JsonResponse(res)"""



# Model Object - Single Student Data

# def user_detail(request, pk):
#     user = User.objects.get(id=2)
#     print(user)
#     serializer = UserSerializer(user)
#     print(serializer)
#     print(serializer.data)
#     json_data = JSONRenderer().render(serializer.data)
#     print(json_data)
#     return HttpResponse(json_data, content_type='application/json')

# Query Set - Users List
# def user_list(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     json_data = JSONRenderer().render(serializer.data)
#     return HttpResponse(json_data, content_type='application/json')


# Create User using API
# csrf problem will arise
# to handle csrf we will use csrf_exempt decorator
# @csrf_exempt
# def create_user(request):
#     if request.method == 'POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         serializer = CreateUserSerializer(data=pythondata)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'User Created'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type="applicaton/json")
#         return JsonResponse(serializer.errors, safe=False)
    

# # post method requires csrf token so to avoid csrf token we will need decorator csrf_exempt
# @csrf_exempt
# def user_api(request):
#     if request.method == 'GET':
#         # get json data from request.body
#         json_data = request.body
#         # store json data in buffer
#         stream = io.BytesIO(json_data)
#         # parse json data into python native data type
#         python_data = JSONParser().parse(stream)
#         # check if id is None
#         id = python_data.get('id', None)
#         if id is not None:
#             user = User.objects.get(id=id)
#             # convert model instance to python native data type using serializer class
#             serializer = UserSerializer(user)
#             # render python native data into json using JSONRenderer
#             json_data = JSONRenderer().render(serializer.data)
#             return HttpResponse(json_data, content_type="application/json")
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         # json_data = JSONRenderer().render(serializer.data)
#         return JsonResponse(serializer.data, safe=False)
    

#     # defining procedure for post request
#     if request.method == 'POST':
#         json_data = request.body
#         # store incoming data in buffer
#         stream = io.BytesIO(json_data)
#         # parse incoming data to native python data type
#         pythondata = JSONParser().parse(stream)
#         # convert native python data to complex data type or model instance
#         serializer = UserSerializer(data=pythondata)
#         # check if data is valid or not
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'User Created'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type="application/json")
#         return JsonResponse(serializer.errors, safe=False)
    

#     # procedure to handle put request
#     if request.method == 'PUT':
#         json_data = request.body
#         # store json data in buffer
#         stream = io.BytesIO(json_data)
#         # parse json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         # get id of the object to be updated
#         id = pythondata.get('id')
#         #Get the object
#         user = User.objects.get(id=id)
#         # use serializer to update data of the instance
#         serializer = UserSerializer(user, data=pythondata, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'User updated'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type="application/json")
#         return JsonResponse(serializer.errors, safe=False)
        
#     # code to handle delete request
#     if request.method == 'DELETE':
#         json_data = request.body
#         # store json_data in the buffer
#         stream = io.BytesIO(json_data)
#         # parse json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         # getting id of the object
#         id = pythondata.get('id')
#         # getting object to be deleted
#         user = User.objects.get(id=id)
#         user.delete()
#         res = {'msg': 'User Deleted!!'}
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type="application/json")






# class PostModelPermissions(DjangoObjectPermissions):
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
#         'HEAD': ['%(app_label)s.view_%(model_name)s'],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }


#     logger.info('in PostModelPermissions')

#     def has_permission(self, request, view):
#         if request.method == 'GET':
#             return request.user.is_authenticated
#         elif request.method == 'POST':
#             return True

#     def has_object_permission(self, request, view, obj):
#         logger.info('in PostModelPermissions has_object_permission')
#         print('permissions.SAFE_METHODS: ', permissions.SAFE_METHODS)
#         breakpoint()
#         return True
#         if request.method in permissions.SAFE_METHODS:
#             # return request.user == obj.owner or True # need to modify so can see own stuff
#             # breakpoint()
#             return request.user.id == obj.post_user.id or True # need to modify so can see own stuff
#         elif request.method == 'PATCH':
#             # return request.user == obj.owner
#             # breakpoint()
#             return request.user.id == obj.post_user.id or request.user.is_staff
#         elif request.method == 'DELETE':
#             # return request.user == obj.owner
#             return request.user.id == obj.post_user.id or request.user.is_staff
#         elif request.method == 'PUT':
#             return request.user.id == obj.post_user.id or request.user.is_staff
#         return False
    
#     def has_change_permission(self, request, view, obj):
#         breakpoint()
#         return True
    
#     def has_delete_permission(self, request, view, obj):
#         breakpoint()
#         return True

    


# class PostModelViewSet(viewsets.ModelViewSet):
#     # queryset = PostModel.objects.all()
#     serializer_class = PostHyperlinkedSerializer

#     def get_queryset(self):
#         # breakpoint()
#         print(reverse('post_api:post-detail', kwargs={'pk': 5} ))
#         return PostModel.objects.all()
    

# class SampleModelPermissions(DjangoObjectPermissions):
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
#         'HEAD': ['%(app_label)s.view_%(model_name)s'],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }

#     logger.info('in SampleModelPermissions')

#     def has_permission(self, request, view):
#         logger.info('in SampleModelPermissions has_permission')
#         # if request.method in permissions.SAFE_METHODS:
#         if request.method in permissions.SAFE_METHODS:
#             logger.info('SampleModelPermissions: has_permission: listing samples for user: ' + str(request.user.id))
#             return True
#         elif request.method == 'POST':
#             suggested_owner = None
#             try:
#                 logger.info('SampleModelPermissions: has_permission: request dict should have a suggested owner: ' + str(dict(request.data.iterlists())))
#                 # breakpoint()
#                 suggested_owner = int(dict(request.data.lists())['owner_id'][0])
#             except:
#                 logger.error('SampleModelPermissions: has_permission: request made without owner_id: ' + str(dict(request.data.lists())))
#                 return False
#             return request.user.id == suggested_owner

#     def has_object_permission(self, request, view, obj):
#         logger.info('in SampleModelPermissions has_object_permission')
#         print('permissions.SAFE_METHODS: ', permissions.SAFE_METHODS)
#         if request.method in permissions.SAFE_METHODS:
#             # return request.user == obj.owner or True # need to modify so can see own stuff
#             # breakpoint()
#             return request.user.id == obj.post_user.id or True # need to modify so can see own stuff
#         elif request.method == 'PATCH':
#             # return request.user == obj.owner
#             return request.user.id == obj.post_user.id
#         elif request.method == 'DELETE':
#             # return request.user == obj.owner
#             return request.user.id == obj.post_user.id
#         return False

# class PostList(ListAPIView):
#     queryset = PostModel.objects.all()
#     # serializer_class = PostSerializer
#     serializer_class = PostHyperlinkedSerializer
#     pagination_class = MyCursorPagination
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    # filter_backends = [OrderingFilter]
    # ordering_fields = ['post_title', 'id']
    # search_fields = ['^post_title']
    # pagination_class = MyPageNumberPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['post_title', 'post_user_id']





# class PostModelViewSet(viewsets.ModelViewSet):
#     # queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         posts = PostModel.objects.filter(post_user_id=self.request.user.id)
#         return posts





# class PostList(ListAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'postscope'

# class PostModelViewSet(viewsets.ModelViewSet):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     throttle_classes = [AnonRateThrottle, JackRateThrottle]


# class PostModelViewSet(viewsets.ModelViewSet):
#     queryset = PostModel.objects.all()
    # serializer_class = PostSerializer
    # authentication_classes = [SessionAuthentication]
    # authentication_classes = [TokenAuthentication]
    # authentication_classes = [CustomAuthentication]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    # permission_classes = [MyPermission]





# class PostModelViewSet(viewsets.ModelViewSet):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAdminUser]

# class PostReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer


# class PostViewSet(viewsets.ViewSet):
#     def list(self, request):
#         posts = PostModel.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         print("**********List**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         print("**********Retrieve**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         id = pk
#         if id is not None:
#             post = PostModel.objects.get(pk=id)
#             serializer = PostSerializer(post)
#             return Response(serializer.data)
        
#     def create(self, request):
#         serializer = PostSerializer(data=request.data)
#         print("**********Create**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Created!!'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def update(self, request, pk):
#         post = PostModel.objects.get(pk=pk)
#         serializer = PostSerializer(post, data=request.data)
#         print("**********Update**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Updated!!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def partial_update(self, request, pk):
#         post = PostModel.objects.get(pk=pk)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         print("**********Partial Update**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Updated Partially!!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk):
#         post = PostModel.objects.get(pk=pk)
#         print("**********Destroy**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         post.delete()
#         return Response({'msg': 'Post Deleted!!'})




# class ListCreatePost(ListCreateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class RetrieveUpdateDestroyPost(RetrieveUpdateDestroyAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer



# class CreateListPost(ListCreateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class RetrieveUpdatePost(RetrieveUpdateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class RetrieveDestroyPost(RetrieveDestroyAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer



# code for concrete api view


# class PostList(ListAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer


# class PostCreate(CreateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class PostDetail(RetrieveAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class UpdatePost(UpdateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class DeletePost(DestroyAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer





"""class PostAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            post = PostModel.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        posts = PostModel.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        id = pk
        post = PostModel.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id = pk
        post = PostModel.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        pdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated Partially !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        id = pk
        post = PostModel.objects.get(id=id)
        post.delete()
        return Response({'msg': 'Post Deleted !!'})"""


"""@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def PostApi(request, pk=None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            post = PostModel.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        posts = PostModel.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Created!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        id = pk
        post = PostModel.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated!!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        id = pk
        post = PostModel.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated Partially !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        id = pk
        post = PostModel.objects.get(id=id)
        post.delete()
        return Response({'msg': 'Post Deleted !!'})"""























# @api_view()
# @authentication_classes([])
# @permission_classes([])
# def hello_world(request):
#     pdb.set_trace()
#     print('userinfo')
#     print(request.user)
#     return Response({'msg': 'This is a get request'})


# @api_view(['POST'])
# @authentication_classes([])
# @permission_classes([])
# def hello_world(request):
#     print(request.data)
#     return Response({'msg':'This is a post request.'})

# @api_view(['GET', 'POST'])
# @authentication_classes([])
# @permission_classes([])
# def hello_world(request):
#     if request.method == 'GET':
#         return Response({'msg': 'This is a GET Request'})
    
#     if request.method == 'POST':
#         print(request.data)
#         return Response({'msg': 'This is a POST Request', 'data': request.data})
# def post_info(request, pk):
#     post = PostModel.objects.get(id=pk)
#     serializer = PostSerializer(post)
#     # json_data = JSONRenderer().render(serializer.data)
#     # return HttpResponse(json_data, content_type="application/json")
#     return JsonResponse(serializer.data)

# def post_list(request):
#     posts = PostModel.objects.all()
#     serializer = PostSerializer(posts, many=True)
#     return JsonResponse(serializer.data, safe=False)

# View to store post info using api
# here we will use csrf_exempt decorator to allow storing data without csrf
    

# api to send information of post
# @csrf_exempt
# def post_api(request):
#     if request.method == 'GET':
#         json_data = request.body
#         # store json data in buffer
#         stream = io.BytesIO(json_data)
#         # parse json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         id = pythondata.get('id', None)
#         if id is not None:
#             post = PostModel.objects.get(id=id)
#             # convert complex type into python native data type
#             serializer = PostSerializer(post)
#             # render native data to json data
#             json_data = JSONRenderer().render(serializer.data)
#             return HttpResponse(json_data, content_type='application/json')
#         posts = PostModel.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     if request.method == 'POST':
#         json_data = request.body
#         # store json_data into the buffer
#         stream = io.BytesIO(json_data)
#         # parse json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         # convert native data into complex data or model instance
#         pdb.set_trace()
#         # user = User.objects.get(id=pythondata.get('post_user_id'))
#         # serializer = UserSerializer(user)
#         # pythondata['post_user'] = serializer.data
#         # pythondata.pop('post_user_id')
#         serializer = PostSerializer(data=pythondata)
#         breakpoint()
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Post Created'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         return JsonResponse(serializer.errors, safe=False)
    

#     # Define procedure for put request
#     if request.method == 'PUT':
#         json_data = request.body
#         # store json_data in buffer
#         stream = io.BytesIO(json_data)
#         breakpoint()
#         # parse json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         # Getting id of the post to be updated
#         id = pythondata.get('id')
#         #Getting the post to be updated
#         post = PostModel.objects.get(id=id)
#         # Use serializer to update the data of post using api
#         breakpoint()
#         serializer = PostSerializer(post, data=pythondata, partial=True)
#         pdb.set_trace()
#         print("breakpoint")
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Post Updated'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         return JsonResponse(serializer.errors, safe=False)
    
#     # code to handle delete request
#     if request.method == 'DELETE':
#         json_data = request.body
#         # storing json data into buffer
#         stream = io.BytesIO(json_data)
#         # parsing json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         # getting id of the post to be deleted
#         id = pythondata.get('id')
#         # getting post to be deleted
#         post = PostModel.objects.get(id=id)
#         post.delete()
#         res = {'msg': 'Post Deleted!!'}
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type="application/json")
    
# class PostModelPermissions(DjangoObjectPermissions):
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
#         'HEAD': ['%(app_label)s.view_%(model_name)s'],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }

#     logger.info('in PostModelPermissions')

#     def has_permission(self, request, view):
#         if request.method == 'GET':
#             return request.user.is_authenticated
#         elif request.method == 'POST':
#             return True

#     def has_object_permission(self, request, view, obj):
#         logger.info('in PostModelPermissions has_object_permission')
#         print('permissions.SAFE_METHODS: ', permissions.SAFE_METHODS)
#         breakpoint()
#         return True
#         if request.method in permissions.SAFE_METHODS:
#             # return request.user == obj.owner or True # need to modify so can see own stuff
#             # breakpoint()
#             return request.user.id == obj.post_user.id or True # need to modify so can see own stuff
#         elif request.method == 'PATCH':
#             # return request.user == obj.owner
#             # breakpoint()
#             return request.user.id == obj.post_user.id or request.user.is_staff
#         elif request.method == 'DELETE':
#             # return request.user == obj.owner
#             return request.user.id == obj.post_user.id or request.user.is_staff
#         elif request.method == 'PUT':
#             return request.user.id == obj.post_user.id or request.user.is_staff
#         return False
    
#     def has_change_permission(self, request, view, obj):
#         breakpoint()
#         return True
    
#     def has_delete_permission(self, request, view, obj):
#         breakpoint()
#         return True





# class PostModelViewSet(viewsets.ModelViewSet):
#     # queryset = PostModel.objects.all()
#     serializer_class = PostHyperlinkedSerializer

#     def get_queryset(self):
#         # breakpoint()
#         print(reverse('post_api:post-detail', kwargs={'pk': 5} ))
#         return PostModel.objects.all()
    

# class SampleModelPermissions(DjangoObjectPermissions):
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
#         'HEAD': ['%(app_label)s.view_%(model_name)s'],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }

#     logger.info('in SampleModelPermissions')

#     def has_permission(self, request, view):
#         logger.info('in SampleModelPermissions has_permission')
#         # if request.method in permissions.SAFE_METHODS:
#         if request.method in permissions.SAFE_METHODS:
#             logger.info('SampleModelPermissions: has_permission: listing samples for user: ' + str(request.user.id))
#             return True
#         elif request.method == 'POST':
#             suggested_owner = None
#             try:
#                 logger.info('SampleModelPermissions: has_permission: request dict should have a suggested owner: ' + str(dict(request.data.iterlists())))
#                 # breakpoint()
#                 suggested_owner = int(dict(request.data.lists())['owner_id'][0])
#             except:
#                 logger.error('SampleModelPermissions: has_permission: request made without owner_id: ' + str(dict(request.data.lists())))
#                 return False
#             return request.user.id == suggested_owner

#     def has_object_permission(self, request, view, obj):
#         logger.info('in SampleModelPermissions has_object_permission')
#         print('permissions.SAFE_METHODS: ', permissions.SAFE_METHODS)
#         if request.method in permissions.SAFE_METHODS:
#             # return request.user == obj.owner or True # need to modify so can see own stuff
#             # breakpoint()
#             return request.user.id == obj.post_user.id or True # need to modify so can see own stuff
#         elif request.method == 'PATCH':
#             # return request.user == obj.owner
#             return request.user.id == obj.post_user.id
#         elif request.method == 'DELETE':
#             # return request.user == obj.owner
#             return request.user.id == obj.post_user.id
#         return False

# class PostList(ListAPIView):
#     queryset = PostModel.objects.all()
#     # serializer_class = PostSerializer
#     serializer_class = PostHyperlinkedSerializer
#     pagination_class = MyCursorPagination
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    # filter_backends = [OrderingFilter]
    # ordering_fields = ['post_title', 'id']
    # search_fields = ['^post_title']
    # pagination_class = MyPageNumberPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['post_title', 'post_user_id']





# class PostModelViewSet(viewsets.ModelViewSet):
#     # queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         posts = PostModel.objects.filter(post_user_id=self.request.user.id)
#         return posts





# class PostList(ListAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'postscope'

# class PostModelViewSet(viewsets.ModelViewSet):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     throttle_classes = [AnonRateThrottle, JackRateThrottle]


# class PostModelViewSet(viewsets.ModelViewSet):
#     queryset = PostModel.objects.all()
    # serializer_class = PostSerializer
    # authentication_classes = [SessionAuthentication]
    # authentication_classes = [TokenAuthentication]
    # authentication_classes = [CustomAuthentication]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    # permission_classes = [MyPermission]





# class PostModelViewSet(viewsets.ModelViewSet):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAdminUser]

# class PostReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer


# class PostViewSet(viewsets.ViewSet):
#     def list(self, request):
#         posts = PostModel.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         print("**********List**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         print("**********Retrieve**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         id = pk
#         if id is not None:
#             post = PostModel.objects.get(pk=id)
#             serializer = PostSerializer(post)
#             return Response(serializer.data)
        
#     def create(self, request):
#         serializer = PostSerializer(data=request.data)
#         print("**********Create**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Created!!'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def update(self, request, pk):
#         post = PostModel.objects.get(pk=pk)
#         serializer = PostSerializer(post, data=request.data)
#         print("**********Update**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Updated!!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def partial_update(self, request, pk):
#         post = PostModel.objects.get(pk=pk)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         print("**********Partial Update**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg': 'Post Updated Partially!!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk):
#         post = PostModel.objects.get(pk=pk)
#         print("**********Destroy**********")
#         print("basename:", self.basename)
#         print("action:", self.action)
#         print("detail:", self.detail)
#         print("suffix:", self.suffix)
#         print("name:", self.name)
#         print("description:", self.description)
#         post.delete()
#         return Response({'msg': 'Post Deleted!!'})




# class ListCreatePost(ListCreateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class RetrieveUpdateDestroyPost(RetrieveUpdateDestroyAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer



# class CreateListPost(ListCreateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class RetrieveUpdatePost(RetrieveUpdateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class RetrieveDestroyPost(RetrieveDestroyAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer



# code for concrete api view


# class PostList(ListAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer


# class PostCreate(CreateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class PostDetail(RetrieveAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class UpdatePost(UpdateAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer

# class DeletePost(DestroyAPIView):
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer








"""class PostAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            post = PostModel.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        posts = PostModel.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        id = pk
        post = PostModel.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id = pk
        post = PostModel.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        pdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated Partially !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        id = pk
        post = PostModel.objects.get(id=id)
        post.delete()
        return Response({'msg': 'Post Deleted !!'})"""


"""@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def PostApi(request, pk=None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            post = PostModel.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        posts = PostModel.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Created!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        id = pk
        post = PostModel.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated!!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        id = pk
        post = PostModel.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated Partially !!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        id = pk
        post = PostModel.objects.get(id=id)
        post.delete()
        return Response({'msg': 'Post Deleted !!'})"""























# @api_view()
# @authentication_classes([])
# @permission_classes([])
# def hello_world(request):
#     pdb.set_trace()
#     print('userinfo')
#     print(request.user)
#     return Response({'msg': 'This is a get request'})


# @api_view(['POST'])
# @authentication_classes([])
# @permission_classes([])
# def hello_world(request):
#     print(request.data)
#     return Response({'msg':'This is a post request.'})

# @api_view(['GET', 'POST'])
# @authentication_classes([])
# @permission_classes([])
# def hello_world(request):
#     if request.method == 'GET':
#         return Response({'msg': 'This is a GET Request'})
    
#     if request.method == 'POST':
#         print(request.data)
#         return Response({'msg': 'This is a POST Request', 'data': request.data})
# def post_info(request, pk):
#     post = PostModel.objects.get(id=pk)
#     serializer = PostSerializer(post)
#     # json_data = JSONRenderer().render(serializer.data)
#     # return HttpResponse(json_data, content_type="application/json")
#     return JsonResponse(serializer.data)

# def post_list(request):
#     posts = PostModel.objects.all()
#     serializer = PostSerializer(posts, many=True)
#     return JsonResponse(serializer.data, safe=False)

# View to store post info using api
# here we will use csrf_exempt decorator to allow storing data without csrf

# api to send information of post
# @csrf_exempt
# def post_api(request):
#     if request.method == 'GET':
#         json_data = request.body
#         # store json data in buffer
#         stream = io.BytesIO(json_data)
#         # parse json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         id = pythondata.get('id', None)
#         if id is not None:
#             post = PostModel.objects.get(id=id)
#             # convert complex type into python native data type
#             serializer = PostSerializer(post)
#             # render native data to json data
#             json_data = JSONRenderer().render(serializer.data)
#             return HttpResponse(json_data, content_type='application/json')
#         posts = PostModel.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     if request.method == 'POST':
#         json_data = request.body
#         # store json_data into the buffer
#         stream = io.BytesIO(json_data)
#         # parse json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         # convert native data into complex data or model instance
#         pdb.set_trace()
#         # user = User.objects.get(id=pythondata.get('post_user_id'))
#         # serializer = UserSerializer(user)
#         # pythondata['post_user'] = serializer.data
#         # pythondata.pop('post_user_id')
#         serializer = PostSerializer(data=pythondata)
#         breakpoint()
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Post Created'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         return JsonResponse(serializer.errors, safe=False)
    

#     # Define procedure for put request
#     if request.method == 'PUT':
#         json_data = request.body
#         # store json_data in buffer
#         stream = io.BytesIO(json_data)
#         breakpoint()
#         # parse json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         # Getting id of the post to be updated
#         id = pythondata.get('id')
#         #Getting the post to be updated
#         post = PostModel.objects.get(id=id)
#         # Use serializer to update the data of post using api
#         breakpoint()
#         serializer = PostSerializer(post, data=pythondata, partial=True)
#         pdb.set_trace()
#         print("breakpoint")
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Post Updated'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         return JsonResponse(serializer.errors, safe=False)
    
#     # code to handle delete request
#     if request.method == 'DELETE':
#         json_data = request.body
#         # storing json data into buffer
#         stream = io.BytesIO(json_data)
#         # parsing json data into python native data type
#         pythondata = JSONParser().parse(stream)
#         # getting id of the post to be deleted
#         id = pythondata.get('id')
#         # getting post to be deleted
#         post = PostModel.objects.get(id=id)
#         post.delete()
#         res = {'msg': 'Post Deleted!!'}
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type="application/json")
    