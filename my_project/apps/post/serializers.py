# from user.serializers import UserSerializer
from rest_framework import serializers
from .models import PostModel
from django.utils import timezone
from rest_framework.response import Response

class PostSerializer(serializers.ModelSerializer):
    pcom = serializers.SlugRelatedField(many=True, read_only=True, slug_field='comment_desc')
    post_user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            # breakpoint()
            return request.user.username
    
    class Meta:
        model = PostModel
        fields = ['id', 'post_title', 'post_description', 'post_content', 'post_date', 'post_user', 'post_likes', 'pcom']
        read_only_fields = ['post_date', 'post_user', 'post_likes']

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