from django import forms
from .models import PostModel, PostComments

class PostForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    content = forms.ImageField()

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['post_title', 'post_description', 'post_content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComments
        fields = ['comment_desc']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = PostComments
        # fields = ['comment_desc', 'com_user', 'com_reply', 'reply_on_comment']
        fields = ['comment_desc', 'reply_on_comment']
