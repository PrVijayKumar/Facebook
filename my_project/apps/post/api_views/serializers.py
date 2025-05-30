# from rest_framework import serializers
# from post.models import PostModel


# class PostHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    
#     class Meta:
#         model = PostModel
#         fields = ['id', 'url', 'post_description']
#         extra_kwargs = {
#             'url': {'view_name': 'postmodel-detail', 'lookup_field': 'id'},
#             # 'url': {'lookup_field': 'id'},
#         }

# print('post_api:postmodel-detail')