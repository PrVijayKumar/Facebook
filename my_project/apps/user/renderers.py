# renderers.py
from rest_framework.renderers import BrowsableAPIRenderer

class MyBrowsableAPIRenderer(BrowsableAPIRenderer):

    """
    Only render the browsable API if there is no 404 error
    """

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)

        response = args[2]['response']
        user = args[2]['request'].user
        # breakpoint()
        if not user.is_superuser:
            # context['raw_data_post_form'].fields.pop('password')
            # context.pop('post_form').fields.pop('password')
            pass
        
        if not user.is_staff: # and 'UserSerializer' in str(context['view'].serializer_class):
            # for field in context['raw_data_post_form'].fields:
            context.pop('raw_data_post_form')
            context.pop('post_form')
        breakpoint()
        if response.status_code == 404:
            # do not display PUT form
            context['display_edit_forms'] = False

        return context

    def get_rendered_html_form(self, data, view, method, request):
        """
        {
            "detail": "Not found."
        }
        """
        if 'detail' in data:
            return
        return super().get_rendered_html_form(data, view, method, request)