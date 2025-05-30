from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
CustomUser = get_user_model()


class Command(BaseCommand):


    help = "Delete inactive user"
    
    def handle(self, *args, **kwargs):
        
        # print(args)
        # print(kwargs)
        # users = kwargs['users']
        users = CustomUser.objects.all()
        for user in users:
            last_login = user.last_login
            current_time = timezone.now()
            if last_login is None:
                days = (current_time-user.date_joined).days
            else:
                days = (current_time-last_login).days

            
            if days > 15:
                user.delete()
                print(f'{user.username} deleted')
            

    # def add_arguments(self, parser):
    #     users = CustomUser.objects.all()
    #     parser.add_argument(
    #         '--users',
    #         type=CustomUser,
    #         default=users,
    #         help='List of Users'
    #     )

        # parser.add_argument(
        #     '--number of users',
        #     type=int,
        #     default=1,
        #     help='Indicates the number of users to be created'
        # )


        # parser.add_argument(
        #     '--type of user',
        #     type=str,
        #     default=1,
        #     choices=RoleChoices,
        #     help='Indicates the number of users to be created'
        # )