# from user.serializers import UserSerializer
from rest_framework import serializers
# from .models import PostModel, PostComments, PostLikes
from .models import PostModel, PostComments
from django.utils import timezone
from rest_framework.response import Response


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComments
        fields = ['id', 'comment_desc', 'com_date', 'post', 'com_user']
        read_only_fields = ['com_user']


class CommentSerializer(serializers.ModelSerializer):
    # replies = serializers.SlugRelatedField(many=True, read_only=True, slug_field='comment_desc')
    Replies = ReplySerializer(many=True, read_only=True, source='replies')
    Replies = ReplySerializer(many=True, read_only=True, source='replies')

    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # breakpoint()
        # mypost = PostModel.objects.get(post_title="Dummy Post")
        # self.fields['reply_on_comment'].choices = [(None, 'None')] + [(reply.id, reply.comment_desc) for reply in PostComments.objects.all().filter(post=getattr(self.instance, 'post', None))]
        # self.fields['reply_on_comment'].choices = [(None, 'None')] + [(reply.id, reply.comment_desc) for reply in PostComments.objects.all()]
        # self.fields['reply_on_comment'].queryset = PostComments.objects.all().filter(post=getattr(self.instance, 'post', None))
        # self.fields['reply_on_comment'].queryset = PostComments.objects.all().filter(post_id=mypost.id)

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            # breakpoint()
            return request.user.username
        
    class Meta:
        model = PostComments
        fields = ['id', 'comment_desc', 'com_date', 'post', 'com_user', 'Replies', 'reply_on_comment']
        read_only_fields = ['com_user']
    # post_title = serializers.SlugRelatedField(read_only=True, slug_field='post_title')
    # post_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    # class Meta:
    #     model = PostComments
    #     fields = ['id', 'comment_desc', 'com_date', 'post_id', 'com_user', 'post_user', 'post_title']
    #     read_only_fields = ['com_date', 'post_id', 'com_user']
    
    def create(self, validated_data):
        validated_data['com_user'] = self.context['request'].user
        # breakpoint()
        
        if validated_data['reply_on_comment'] is not None:
            if validated_data['reply_on_comment'].post.id != validated_data['post'].id:
                validated_data['post'] = PostModel.objects.get(id=validated_data['reply_on_comment'].post.id)
            # validated_data['reply_on_comment'] = validated_data['reply_on_comment']
        # else:
        # validated_data['post_id'] = self.context['post']
        return super().create(validated_data)

# class CreateReplySerializer(serializers.Serializer):
#     comment_desc = serializers.CharField(max_length=200)
#     post = serializers.IntegerField()
#     com_user = serializers.IntegerField(default=1)
#     reply_on_comment = serializers.IntegerField(default=None, allow_null=True)

#     def create(self, valid_data):
#         return PostComments.objects.create(**valid_data)
    


class PostSerializer(serializers.ModelSerializer):
    pcom = serializers.SlugRelatedField(many=True, read_only=True, slug_field='comment_desc')
    post_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    is_liked = serializers.SerializerMethodField()
    # like_count = serializers.SerializerMethodField()
    # likes = serializers.PrimaryKeyRelatedField(many=True, queryset=PostLikes.objects.all(), source='post_likes')

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            # breakpoint()
            return request.user.username
    
    class Meta:
        model = PostModel
        fields = ['id', 'post_title', 'post_description', 'post_content', 'post_date', 'post_user', 'like_count', 'pcom', 'is_liked']
        # fields = ['id', 'post_title', 'post_description', 'post_content', 'post_date', 'post_user', 'post_likes', 'pcom']
        read_only_fields = ['post_date', 'post_user', 'like_count']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.post_likes.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        # breakpoint()
        validated_data['post_user'] = self.context['request'].user
        return super().create(validated_data)
        

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # self.current_user = self._user(self)
    #     breakpoint()
    #     self.fields['current_user'].disabled = True

        # create_only_fields = ['current_uesr']
        # extra_kwargs = {
        #     'current_user': {
        #         'default': serializers.SerializerMethodField('_user'),
        #     }
        # }
    # current_user = serializers.SerializerMethodField('_user')
    # current_user = serializers.CharField(max_length=255)
    # post_user = serializers.ChoiceField(default='vijay', choices=('vijay', 'namo'))

    # def _user(self, obj):
    #     request = self.context.get('request', None)
    #     if request:
    #         return str(request.user)



# def post_starts_with_p(value):
#     if value[0].lower() != 'p':
#         raise serializers.ValidationError("Post must start with P")
#     return value

# class PostSerializer(serializers.ModelSerializer):
#     # post_user = UserSerializer()
#     def start_with_p(value):
#         if value[0].lower() != 'p':
#             raise serializers.ValidationError("Post title must start with p")
    # post_title = serializers.CharField(max_length=100, validators=[start_with_p])
    
    # post_user_id = serializers.IntegerField()
    # post_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    # post_user = serializers.StringRelatedField(read_only=True)
    # post_user = serializers.PrimaryKeyRelatedField(read_only=True)
    # post_user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    # pcom = serializers.SlugRelatedField(many=True, read_only=True, slug_field='comment_desc')
    # class Meta:
    #     model = PostModel
    #     fields = ['id', 'post_title', 'post_description', 'post_date', 'post_user', 'pcom', 'post_likes']

    # def validate_post_user_id(self, value):
    #     if value > 3:
    #         raise serializers.ValidationError('User must have id less than 3')
    #     return value
    
    # def validate(self, data):
    #     pt = data.get('post_title')
    #     pd = data.get('post_description')

    #     if pt.lower() == 'india' and pd.lower() == 'illegal post':
    #         raise serializers.ValidationError('illegal post not allowed')
    #     return data

        
# class PostSerializer(serializers.Serializer):
#     post_title = serializers.CharField(max_length=100, validators=[post_starts_with_p])
#     post_description = serializers.CharField(max_length=100)
#     post_date = serializers.DateTimeField(default=timezone.now)
#     post_user_id = serializers.IntegerField()

#     def create(self, validated_data):
#         return PostModel.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.post_title = validated_data.get('post_title', instance.post_title)
#         instance.post_description = validated_data.get('post_description', instance.post_description)
#         instance.save()
#         return instance
    
#     def validate_post_user_id(self, value):
#         breakpoint()
#         if value > 3:
#             raise serializers.ValidationError('Not Allowed')
#         return value
    
#     def validate(self, data):
#         breakpoint()
#         pt = data.get('post_title')
#         pd = data.get('post_description')

#         if pt.lower() == 'india' and pd.lower() == 'illegal post':
#             raise serializers.ValidationError("Illegal Post Not allowed")
#         return data


class CreatePostSerializer(serializers.Serializer):
    post_title = serializers.CharField(max_length=100)
    post_description = serializers.CharField(max_length=100)
    post_date = serializers.DateTimeField(default=timezone.now)
    post_user_id = serializers.IntegerField(default=1)

    def create(self, valid_data):
        return PostModel.objects.create(**valid_data)