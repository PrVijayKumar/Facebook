from django.contrib import admin
# from .models import User
from .models import CustomUser
# Register your models here.


# admin.site.register(User)
# admin.site.register(Post)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff']
    readonly_fields= ['id']

# admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)


