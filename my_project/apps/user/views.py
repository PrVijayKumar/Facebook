from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm, AuthenticationForm, ResetPassword #  , PostForm
from django.contrib.auth import  login as auth_login, logout as auth_logout, authenticate
# from .customauth.CustomAuthentication import authenticate
from django.contrib.auth.decorators import login_required
from post.models import PostModel, PostLikes
from rest_framework import viewsets
# from .serializers import UserHyperlinkedSerializer
# from .models import User
from .models import CustomUser, Codes, Stars
from email.mime.image import MIMEImage
import pathlib
from user.tasks import user_reg_email, reset_pass_email
import logging
from django.utils import timezone
# from django.template.loader import render_to_string
# Create your views here.
from . import signals
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_page
from django.core.paginator import Paginator
# from .decorators import cache_on_auth
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer = UserHyperlinkedSerializer
logger = logging.getLogger(__name__)


def fpassword(request):
    # if request.method == 'GET':
#         form = ForgotPasswordForm()
    form = AuthenticationForm()

    if request.method == 'POST':
        email = request.POST['email']
        # breakpoint()
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            return HttpResponseRedirect(f"/rpass/{user.id}")
        err_msg = "<strong>No search results</strong><br>\n Your search did not return any results. Please try again with other information."
        
        return render(request, 'user/fpass.html', {'form': form, 'error': err_msg})


    return render(request, 'user/fpass.html', {'form': form})


def rpassword(request, id):
    user = CustomUser.objects.get(id=id)
    value = user.email
    # breakpoint()
    if request.method == 'POST':
        pass
    
    return render(request, 'user/rpass.html', {'value': value, 'id': id})


def rcode(request, id):
    user = CustomUser.objects.get(id=id)
    value = user.email
    # breakpoint()
    if request.method == 'POST':
        if request.POST['ropt'] == '1':
            return render(request, "user/rcode.html")
        elif request.POST['ropt'] == '2':
            result = reset_pass_email.delay(user.username, user.email, user.id)
            return render(request, 'user/ecode.html', {'id': user.id})
        elif request.POST['ropt'] == '3':
            form = AuthenticationForm()
            return render(request, "user/login.html", {'form': form, 'title': login})
    
    # if request.META['HTTP_REFERER'] == f"http://127.0.0.1:8000/user/rcode/{id}" and request.method == 'GET':
        
    #     return redirect(f'./{id}')
    return render(request, 'user/rpass.html', {'value': value, 'id': id})



def vcode(request, id):
    # breakpoint()
    if request.method == 'POST':
        user = CustomUser.objects.get(id=id)
        try:
            code = Codes.objects.get(user_id=user.id)
        except Codes.DoesNotExist:
            # breakpoint()
            # return redirect(f'./{id}')
            return redirect(request.META['HTTP_REFERER'])
            # History.back()
        if code.code == request.POST['rcode']:
            return HttpResponseRedirect(f'/resetpass/{user.id}')
        return redirect(request.META['HTTP_REFERER'])


def resetpass(request, id):

    form = ResetPassword()
    if request.method == 'POST':
        user = CustomUser.objects.get(id=id)
        # breakpoint()
        # if re.search()
        # breakpoint()
        form = ResetPassword(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            try:
                code = Codes.objects.get(user_id=id)
                code.delete()
            except Codes.DoesNotExist:
                pass
            messages.success(request, 'Login with your new password')
            return redirect('user:login-page')
    return render(request, 'user/respass.html', {'id': id, 'form': form})

def register(request):
    # logger = logging.getLogger(__name__)
    # logger = logging.getLogger("myapp")
    # logger = logging.getLogger("geekyshows")
    # logger.debug('This is a dubug message.')
    # logger.info('This is an info message.')
    # logger.warning('This is a warning message.')
    # logger.error('This is an error message.')
    # logger.critical('This is a critical message.')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # breakpoint()
        if form.is_valid():
            form.save()
           
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            result = user_reg_email.delay(username, email)
            # logger
            logger.info(f"New account created for user:{username} on {timezone.now()}")
            messages.success(request, f'Account created for {username}')
            return redirect('user:login-page')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

# @cache_page(60 * 5)
def login(request):
    # breakpoint()
    # send_mail(
    #     'Testing',
    #     'Hy Vijay Choudhary How are you',
    #     'vijaychoudhary@thoughtwin.com',
    #     ['vijay24082000@gmail.com'],
    #     fail_silently=False
    # )

    # text_content = "Hello Vijay Following is your Secret Key"

    # html_content = "<H1>Professor</H1><p>To Become a Professor you should have good <b>communication skills</b> and <i>command on your subject</i></p>"

    # msg = EmailMultiAlternatives(
    #     'Testing Multi Alternatives',
    #     text_content,
    #     'vijaychoudhary@thoughtwin.com',
    #     ['vijay24082000@gmail.com'],
    # )

    # msg.attach_alternative(html_content, 'text/html')
    # num = msg.send()
    # print("Number of mails", num)


    # message1 = (
    #     "First Message",
    #     "Hello mail for understanding send_mass_mail",
    #     "vijaychoudhary@thoughtwin.com",
    #     ["vijay24082000@gmail.com"]
    # )

    # message2 = (
    #     "Second Message",
    #     "Hello sending multple mails at once without opening connection again and again",
    #     "vijaychoudhary@gmail.com",
    #     ["gaurav@thoughtwin.com", "divyanshyadav@thoughtwin.com"]
    # )

    # num = send_mass_mail((message1, message2), fail_silently=False)

    # print(num)

    # email = EmailMessage(
    #     "Example Mail",
    #     "I am learning email through django",
    #     "vijaychoudhary@thoughtwin.com",
    #     ["vijay24082000@gmail.com"],
    #     reply_to=["vijaychoudhary@thoughtwin"],
    #     headers={"My-Header": "This is a header"}
    # )
    # breakpoint()
    # print(pathlib.Path(__file__).parent.parent.parent.resolve()/'media/images'/'crow_1JMfgUW.png')
    path = pathlib.Path(__file__).parent.parent.parent.resolve()/'media/images'/'449195169_1720433388491215_1556072659052802667_n_2axw1hM.png'
    # img_data = open(path, 'rb').read()
    # msgImg = MIMEImage(img_data, 'png')

    # email.attach(msgImg)
    # email.attach_file('../../../media/images/449195169_1720433388491215_1556072659052802667_n_2axw1hM.png')
    # num = email.send(fail_silently=False)
    # print(email.message())
    # print(email.recipients())
    # print(num)
    


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # user = authenticate(request, username=username, password=password)
        # breakpoint()
        if user is not None:
            signals.create_dummy_post.send(sender=CustomUser, user=user)
            form = auth_login(request, user)
            # auth_login(request, user)
            messages.success(request, f"Welcome {username}")
            # # breakpoint()
            return redirect('/allposts/')
            # return render(request, '/user/allposts/', {'form': form})
        else:
            messages.error(request, 'Incorrect Username or Password')
            logger.warning(f'User enterered wrong username:{username} and password:{password}')
            # print(__name__)
    form = AuthenticationForm()
    return render(request, "user/login.html", {'form': form, 'title': login})
    # return redirect('/')


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return HttpResponseRedirect(reverse('user:login-page'))
        # return redirect('user:login-page')

@login_required
def dashboard(request):
    # username = request.POST['username']
    # context = {}
    # return render(request, '/user/mypost.html', {'context': context})
    # return HttpResponse("Elocome")
    context = {}
    ulikes = []
    posts = PostModel.objects.all().order_by('-post_date')
    # likes = PostLikes.objects.filter(liked_by=request.POST['user'])
    likes = PostLikes.objects.filter(liked_by=request.user.id)
    for like in likes:
        ulikes.append(like.post_id_id)
    # print(likes)
    print(ulikes)
    context['posts'] = posts
    context['likes'] = likes
    context = {
        'posts': posts,
        'likes': ulikes,
    }
    return render(request, 'user/allposts.html', context)
    # return render(request, 'user/allposts.html')

# def mypost(request):
#     context = {}
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             title = form.cleaned_data.get("title")
#             content = form.cleaned_data.get("content")
#             obj = PostModel.objects.create(
#                 post_title=title,
#                 post_content=content
#             )
#             obj.save()
#             print(obj)
#             messages.success(request, f'Post sent succesfully')
#             return HttpResponseRedirect("/user/dashboard")
#     else:
#         form = PostForm()
#     context['form'] = form
#     return render(request, 'user/post.html', context)

# def all_posts(request):
#     posts = PostModel.objects.all().order_by('-post_date')
#     context={}
#     context={
#         'posts': posts
#     }
#     return render(request, 'user/allposts.html', context)
# @never_cache
# @cache_page(60 * 10)
def all_posts(request):
    stars = Stars.objects.filter(user_id=request.user.id)
    nos = 0
    if not stars:
        if isinstance(request.user, CustomUser):
            new_star = Stars.objects.create(user=request.user)
            new_star.save()
    else:
        new_star = Stars.objects.get(user_id=request.user)
        nos = new_star.amount
    context = {}
    ulikes = []
    posts = PostModel.objects.all().order_by('-post_date')
    # likes = PostLikes.objects.filter(liked_by=request.POST['user'])
    likes = PostLikes.objects.filter(liked_by=request.user.id)
    # breakpoint()
    pages = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = pages.get_page(page_number)
    if likes:
        for like in likes:
            ulikes.append(like.post_id_id)
    # print(likes)
    print(ulikes)
    context['posts'] = posts
    context['likes'] = likes
    context = {
        'posts': posts,
        'likes': ulikes,
        'page_obj': page_obj,
        'total_pages': range(page_obj.paginator.num_pages),
        'nos': nos
    }
    return render(request, 'user/allposts.html', context)
    # return HttpResponse("Hello from all posts")
