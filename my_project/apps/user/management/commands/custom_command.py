from django.core.management.base import BaseCommand



class Command(BaseCommand):

    help = "This will print hello world!"


    def handle(self, *args, **kwargs):
        print("Hi, there !")

    # help = "create new user "
    
    # def handler(self, *args, **kwargs):
    #     pass

    # def add_arguments(self, parser):

    #     parser.add_argument(
    #         'role_type',
    #         type=str,
    #         help='Indicate role name'
    #     )

    #     parser.add_argument(
    #         '--number of users',
    #         type=int,
    #         default=1,
    #         help='Indicates the number of users to be created'
    #     )