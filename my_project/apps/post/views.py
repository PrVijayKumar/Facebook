from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import PostForm, PostUpdateForm, CommentForm, ReplyForm
from .models import PostModel, CustomUser as User, PostLikes, timezone, PostComments, PostStars  # , NotEqual, Field
# from .models import PostModel, CustomUser as User, PostLikes, timezone, PostComments, Stars, Price  # , NotEqual, Field
# from .models import PostModel, User, PostLikes, timezone, PostComments  # , NotEqual, Field
import json
import datetime
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import CustomUser, Stars, StarsPaymentLogs
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from django.core.paginator import Paginator

stripe.api_key = settings.STRIPE_SECRET_KEY
# DOMAIN = settings.DOMAIN

logger = logging.getLogger(__name__)
# from django.core import serializers
# from django.core.serializers.get_serializer

# def remove_circular_refs(ob, _seen=None):
#     if _seen is None:
#         _seen = set()
#     if id(ob) in _seen:
#         # circular reference, remove it.
#         return None
#     _seen.add(id(ob))
#     res = ob
#     if isinstance(ob, dict):
#         res = {
#             remove_circular_refs(k, _seen): remove_circular_refs(v, _seen)
#             for k, v in ob.items()}
#     elif isinstance(ob, (list, tuple, set, frozenset)):
#         res = type(ob)(remove_circular_refs(v, _seen) for v in ob)
#     # remove id again; only *nested* references count
#     _seen.remove(id(ob))
#     return res

# class MyEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, datetime.datetime):
#             if isinstance(o, datetime.datetime):
#                 return dict(year=o.year, month=o.month, day=o.day)
#             else:
#                 json.JSONEncoder.default(self, o)
#         elif isinstance(o, int):
#             return json.dumps(o)
#         elif isinstance(o, User):
#             return str(o)
#         else:
#             return o.__dict__


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if (isinstance(obj, datetime.datetime) or isinstance(obj, int) or isinstance(obj, User)):
            return str(obj)
        return super().default(obj)





# Create your views here.




def create_post(request):
    # breakpoint()
    context = {}
    if request.method == 'POST' and request.user.is_authenticated:
        form = PostForm(request.POST, request.FILES)
        # breakpoint()
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            content = form.cleaned_data.get('content')
            print(content)
            obj = PostModel(
                    post_title=title,
                    post_description=description,
                    post_content=content,
                    post_user=request.user
                )
            print(request.user)
            obj.save()
            messages.success(request, 'Post sent successfully.')
            # logger message for new post creation
            logger.info(f"New post with title: {obj.post_title} created by user: {request.user.username} on {timezone.now()}")
            print("data submit")
            return HttpResponseRedirect('/allposts')
    else:
        form = PostForm()
    context['form'] = form
    return render(request, "post/createpost.html", context)
    # return HttpResponse("Create post page")


def my_posts(request):
    # Initialize an empty context dictionary to pass data to the template
    context = {}

    # Fetch the user's stars from the database
    stars = Stars.objects.filter(user_id=request.user.id)
    nos = 0  # Initialize the number of stars to 0

    # If the user has no stars, create a new Stars object for them
    if not stars:
        new_star = Stars.objects.create(user=request.user)
        new_star.save()
    else:
        # Otherwise, fetch the existing Stars object and get the amount of stars
        new_star = Stars.objects.get(user_id=request.user)
        nos = new_star.amount

    # Get the current logged-in user
    c_user = request.user
    print(c_user)  # Debugging: Print the current user

    # Fetch posts created by the current user, ordered by the most recent post date
    posts = PostModel.objects.filter(post_user=c_user.id).order_by('-post_date')

    # Paginate the posts, showing 5 posts per page
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')  # Get the current page number from the request
    PostsFinal = paginator.get_page(page_number)  # Get the posts for the current page
    totalpages = PostsFinal.paginator.num_pages  # Get the total number of pages

    # Fetch the posts liked by the current user
    likes = PostLikes.objects.filter(liked_by_id=request.user.id)
    ulikes = []  # Initialize an empty list to store liked post IDs

    # Add the IDs of liked posts to the list
    for like in likes:
        ulikes.append(like.post_id_id)

    print(ulikes)  # Debugging: Print the list of liked post IDs

    # Prepare the context dictionary with data to render in the template
    context = {
        'posts': PostsFinal,  # Paginated posts
        'lastpage': totalpages,  # Total number of pages
        'likes': ulikes,  # List of liked post IDs
        'totalPageList': [n+1 for n in range(totalpages)],  # List of page numbers
        'nos': nos,  # Number of stars the user has
    }

    # Render the 'myposts.html' template with the context data
    return render(request, 'post/myposts.html', context)


# def all_posts(request):
#     breakpoint()
#     context = {}
#     posts = PostModel.objects.all().order_by('-post_date')
#     likes = PostLikes.objects.all()
#     context['posts'] = posts
#     context['likes'] = likes
#     # breakpoint()
#     # import inspect
#     # print(inspect.stack()[1])
#     # breakpoint()
#     return render(request, 'post/allposts.html', context)

def friend_posts(request):
    context = {}
    stars = Stars.objects.filter(user_id=request.user.id)
    nos = 0
    if not stars:
        new_star = Stars.objects.create(user=request.user)
        new_star.save()
    else:
        new_star = Stars.objects.get(user_id=request.user)
        nos = new_star.amount
    ulikes = []
    c_user = request.user
    posts = PostModel.objects.all().exclude(post_user=c_user.id).order_by('-post_date')
    likes = PostLikes.objects.filter(liked_by=request.user.id)
    if likes:
        for like in likes:
            ulikes.append(like.post_id_id)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    PostsFinal = paginator.get_page(page_number)
    totalpages = PostsFinal.paginator.num_pages #3
    # context['posts'] = posts
    context = {
        # 'posts': posts,
        'posts': PostsFinal,
        'lastpage': totalpages,
        'totalPageList': [n+1 for n in range(totalpages)],
        'nos': nos,
        'likes': ulikes,
    }
    return render(request, 'post/friends_post.html', context)


# def edit_posts(request, id):
#     obj = PostModel.objects.get(pk=id)
#     context = {}
#     if request.method == 'POST':
#         form = PostUpdateForm(request.POST, request.FILES, initial={'post_content': obj.post_content, 'post_description': obj.post_description, 'post_title': obj.post_title})
#         if form.is_valid():
#             obj.post_title = form.cleaned_data.get('post_title')
#             obj.post_description = form.cleaned_data.get('post_description')
#             obj.post_content = form.cleaned_data.get('post_content')
#             obj.save()
#             messages.success(request, "Post Updated Successfully.")
#             return HttpResponseRedirect('/user/dashboard/')
#     else:
#         form = PostUpdateForm(instance=obj)
#         print(obj.post_content, obj.post_title, obj.post_description)
#     context = {
#         'form': form
#     }
#     return render(request, 'post/editpost.html', context)

# def edit_posts(request, id):
#     obj = PostModel.objects.get(pk=id)
#     context = {}
#     print(request.POST)
#     if request.method == 'POST':
#         form = PostUpdateForm(request.POST, request.FILES, initial={'post_content': obj.post_content, 'post_description': obj.post_description, 'post_title': obj.post_title})
#         if form.is_valid():
#             obj.post_title = form.cleaned_data.get('post_title')
#             obj.post_description = form.cleaned_data.get('post_description')
#             # print(request.POST['post_content'])
#             obj.post_content = form.cleaned_data.get('post_content')
#             obj.post_updated_date = timezone.now()
#             # print(obj.post_content)
#             obj.save()
#             messages.success(request, "Post Updated Successfully.")
#             # return HttpResponseRedirect('/post/myposts/')
#             # return HttpResponseRedirect(request.META['HTTP_REFERER'])
#             return JsonResponse("Hello from edit posts.")
#     else:
#         form = PostUpdateForm(instance=obj)
#         print(obj.post_content, obj.post_title, obj.post_description)
#     context = {
#         'form': form
#     }
#     # return render(request, 'post/editpost.html', context)
#     # return redirect(request.META['HTTP_REFERER'])
#     return JsonResponse("worked")



def del_post(request, id):
    if request.user.is_authenticated:
        # print("hello")
        # breakpoint()
        obj = PostModel.objects.get(pk=id)
        obj.delete()
        # messages.success(request, "Post Deleted.")
        result = json.dumps({'result': 'Deleted', 'id': str(id), 'msg': 'Post Deleted'})

        # logger
        logger.warning(f"Post with title: {obj.post_title} deleted by user: {request.user.username} on {timezone.now()}")
        return JsonResponse({'result': result})
        # return HttpResponseRedirect(reverse('post:mpost'))
        # return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return redirect(reverse('user:login-page'))



def det_post(request, id):
    if request.user.is_authenticated:
        obj = PostModel.objects.get(pk=id)
        context = {
            'post': obj
        }
        return render(request, 'post/detpost.html', context)
    return render(request, 'post/detpost.html')


def like_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            fuser = User.objects.get(pk=request.POST['uid'])
            obj = PostModel.objects.get(pk=id)
            likes = PostLikes()
            print("working")
            # breakpoint()

            # likes = PostLikes.object.get()
            if int(request.POST['flag']) == 1:
                obj.post_likes += 1
                likes.liked_by = fuser
                print(likes.liked_by)
                likes.post_id = obj

                # logger for post like
                logger.info(f"Post with title: {obj.post_title} liked by user: {request.user.username} on {timezone.now()}")
                likes.save()
            else:
                obj.post_likes -= 1
                likes = PostLikes.objects.filter(post_id=id).filter(liked_by=fuser)
                print(likes)
                # logger for post dislike
                logger.warning(f"Post with title: {obj.post_title} disliked by user: {request.user.username} on {timezone.now()}")
                likes.delete()
                # likes.save()
            obj.save()

            print(obj.post_likes)
            return HttpResponse(obj.post_likes)
        elif request.method == "GET":
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return redirect(reverse('user:login-page'))
        # return HttpResponse("post worked")


def edit_posts(request, id):
    if request.user.is_authenticated:
        obj = PostModel.objects.get(pk=id)
        context = {}
        if request.method == 'POST':
            form = PostUpdateForm(request.POST, request.FILES, initial={'post_content': obj.post_content, 'post_description': obj.post_description, 'post_title': obj.post_title})
            # print(request.POST, request.FILES)
            print(form)
            print(form.is_valid())
            if form.is_valid():
                obj.post_title = form.cleaned_data.get('post_title')
                obj.post_description = form.cleaned_data.get('post_description')
                # print(request.POST['post_content'])
                obj.post_content = form.cleaned_data.get('post_content')
                obj.post_updated_date = timezone.now()
                # print(obj.post_content)
                # logger for editing post
                logger.info(f"Post with title: {obj.post_title} successfully edited by user: {request.user.username} on {timezone.now}")
                obj.save()
                # messages.success(request, "Post Updated Successfully.")
                # return HttpResponseRedirect('/post/myposts/')
                # return HttpResponseRedirect(request.META['HTTP_REFERER'])
                # print(MyEncoder().encode(obj))
                # print(isinstance(obj.post_likes, int))
                # x = json.dumps(obj.post_likes)
                # print(type(x))
                # print(obj.post_content)
                # json.dumps(cls=MyEncoder)
                # x=0
                # y=json.dumps(x)
                # print(type(y), type(x))

                # data = serializers.serialize("json", obj)
                # # XMLSerializer = serializers.get_serializer("xml")
                # # xml_serializer = XMLSerializer()
                # # xml_serializer.serialize(obj)
                # # data = xml_serializer.getvalue()
                # print(data)

                result = serialize("json", [obj], cls=LazyEncoder)
                # x = serializers.serialize("json", [obj], indent=2,
                #                       use_natural_foreign_keys=True,
                #                       use_natural_primary_keys=True,)

                # print(x)
                return JsonResponse({"result": result})
        else:
            form = PostUpdateForm(instance=obj)
            print(obj.post_content, obj.post_title, obj.post_description)
        context = {
            'form': form
        }
        # return render(request, 'post/editpost.html', context)
        # return redirect(request.META['HTTP_REFERER'])
        return JsonResponse({"result": "worked"})
    else:
        return redirect(reverse("user:login-page"))

def comment_post(request, id):
    if request.user.is_authenticated:
        # breakpoint()
        result = None
        reply = None
        try:
            reply = request.POST['com_reply']
        except:
            reply = None
        post = PostModel.objects.get(pk=id)
        if request.method == 'POST':
            # breakpoint()
            if reply is not None:
                print(request.user, request.POST['com_reply'])
                com_reply = User.objects.get(username=request.POST['com_reply'])
                print(com_reply)
                form = ReplyForm(request.POST)
                print(form.is_valid())
                if form.is_valid():
                    obj = PostComments(
                        comment_desc=form.cleaned_data.get('comment_desc'),
                        com_user=request.user,
                        post=post,
                        reply_on_comment=form.cleaned_data.get('reply_on_comment'),
                        com_reply=com_reply,
                    )
                    # logger for reply
                    logger.info(f"{request.user.username} replied on comment of {com_reply.username} on post: {post} on {timezone.now()}")
                    obj.save()
                    result = serialize('json', [obj], cls=LazyEncoder)
                print(form)
            else:
                form = CommentForm(request.POST, initial={'com_user': request.user})
                if form.is_valid():
                    obj = PostComments(
                        comment_desc=form.cleaned_data.get('comment_desc'),
                        com_user=request.user,
                        post=post,
                    )
                    obj.save()

                    # logger for comment
                    logger.info(f"{request.user.username} commented on post: {post} on {timezone.now()}")
                    print("Object Id", obj.id)
                    result = serialize('json', [obj], cls=LazyEncoder)
                else:
                    # print("error")
                    # logger for invalid comment
                    logger.warning(f"Invalid comment passed on post: {post.post_title} by user: {request.user.username} on {timezone.now()}")
                    obj = PostComments()
                    result = 'error'
        else:
            result = "error"
            # logger for error
            logger.info(f"{request.user.username} attempted to make comment using GET method.")
        return JsonResponse({'result': result})
    else:
        return redirect(reverse('user:login-page'))


def fetch_comments(request, id):
    if request.user.is_authenticated:
        comments = PostComments.objects.filter(post_id=id).filter(com_reply=None).order_by("-com_date")
        users = User.objects.all().values_list('id', 'username')
        # print(list(users))
        rlist = []
        for comment in comments:
            rlist.append(comment.id)
        mylist = []
        for a in rlist:
            checklist = PostComments.objects.filter(reply_on_comment=a)
            if not checklist:
                pass
            else:
                mylist.append(a)
        # print(mylist)
        rlist = json.dumps(mylist)
        # print(comments)
        # result= 'error'
        # result = serialize('json', [comments], cls=LazyEncoder)  this line will not work because comments 
        # is a set of objects so no need to pass it as dictionary
        result = serialize('json', comments, cls=LazyEncoder)
        # users = serialize('json', users, cls=LazyEncoder)
        try:
            # users = serialize('json', list(users), cls=LazyEncoder)
            users = json.dumps(list(users))
        except:
            logger.warning(f"users not json serializable in fetch_comments")
            print("Error")
        # print(users)
        return JsonResponse({'result': result, 'users': users, 'rlist': rlist})
    else:
        return redirect(reverse('user:login-page'))

def fetch_replies(request, id):
    if request.user.is_authenticated:
        result = None
        replies = PostComments.objects.filter(reply_on_comment=id).order_by('-com_date')
        rstatus = replies.values_list('id')
        rlist = []
        for r in rstatus:
            rlist.append(r[0])
        print(rlist)
        mylist = []
        # breakpoint()
        for a in rlist:
            comments = PostComments.objects.filter(reply_on_comment=a)
            print(comments)
            if not comments:
                pass
            else:
                # breakpoint()
                mylist.append(a)
        print(mylist)
        rlist = json.dumps(mylist)
        users = User.objects.values('id', 'username')
        result = serialize('json', replies, cls=LazyEncoder)
        # users = serialize('json', list(users), cls=LazyEncoder)
        users = json.dumps(list(users))
        # print(result)
        return JsonResponse({'result': result, 'users': users, 'rlist': rlist})
    else:
        return redirect(reverse('user:login-page'))


def edit_comment(request, id):
    # breakpoint()
    if request.user.is_authenticated:
        result = None
        com = PostComments.objects.get(id=id)
        print(com)
        if request.method == 'POST':
            form = CommentForm(request.POST, initial={'comment_desc': com.comment_desc})
            if form.is_valid():
                com.comment_desc = form.cleaned_data.get('comment_desc')
                com.save()
                # logger for editing comments
                logger.info(f"{request.user.username} edited the comment on {timezone.now()}")
                result = serialize('json', [com], cls=LazyEncoder)
        else:
            logger.info(f'{request.user.username} made an attempt to edit comments through get request')
            result = "Error"
        return JsonResponse({'result': result})
    else:
        return redirect(reverse('user:login-page'))


def delete_comment(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # comments = PostComments.objects.filter(reply_on_comment=id)
            # breakpoint()
            # for c in comments:
                # logger for deleting comments
            # print('entered')
            # comments.delete()
            try:
                comment = PostComments.objects.get(id=id)
                comment.delete()
                logger.warning(f"{request.user.username} deleted comment: {comment.comment_desc}")
                # logger.warning(f"{request.user.username} deleted comment: {c.comment_desc}")
                result = json.dumps({'result': 'Deleted', 'id': str(id)})
                return JsonResponse({'result': result})
            except PostComments.DoesNotExist:
                return JsonResponse({'result': 'Comment Does Not Exist'})
            
        elif request.method == 'GET':
            return JsonResponse({'result': 'Error'})
    else:
        return redirect(reverse('user:login-page'))



# class CheckoutView(LoginRequiredMixin, View):
#     def get(self, request, post_id):
#         post = get_object_or_404(PostModel, id=post_id)
#         user = get_object_or_404(CustomUser, id=post.post_user_id)
#         return render(request, "post/checkout.html", {"user": CustomUser})
    

# def success(request):
#     return JsonResponse({'status': "Success"})

# def cancel(request):
#     return JsonResponse({'status': 'Cancel'})


@method_decorator(csrf_exempt, name='dispatch')
class CreatePaymentView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        # breakpoint()
        user = CustomUser.objects.get(email=request.POST['received_by'])
        post = PostModel.objects.get(id=int(request.POST['post']))
        for u in (user, request.user):
            if not Stars.objects.filter(user=u):
                if u == request.user:
                    new_star = Stars.objects.create(user=u, amount=0)
                else:
                    new_star = Stars.objects.create(user=u, amount=int(request.POST['amount']))
                new_star.save()
            else:
                if u == request.user:
                    old_star = Stars.objects.get(user=u)
                    old_star.amount = old_star.amount - int(request.POST['amount'])
                    old_star.save()
                else:
                    old_star = Stars.objects.get(user=u)
                    old_star.amount = old_star.amount + int(request.POST['amount'])
                    old_star.save()

        new_log = StarsPaymentLogs.objects.create(sent_by=request.user, received_by=user, amount=int(request.POST['amount']))
        new_log.save()
        new_stars = PostStars.objects.create(post=post, sent_by=user, nos=int(request.POST['amount']))
        new_stars.save()
        post.post_stars = post.post_stars + int(request.POST['amount'])
        post.save()
        print(request.POST)
        print(request.user.username)

        result = json.dumps({'result': 'Working', 'amount': post.post_stars, 'post_id': post.id})
        return JsonResponse({'result': result})


        # line_items=[{
        #         'price_data': {
        #         'currency': 'usd',
        #         'unit_amount': int(amount_in_rs * 100),
        #         'stars_data': {
        #             'sent_by': request.user
        #         }
        #     },
        #     'quantity': 1,
        #     }],