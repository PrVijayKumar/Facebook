from rest_framework import serializers
# from .models import User
from .models import CustomUser
from post.serializers import PostSerializer
import re

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True, source='postname')
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_staff', 'first_name', 'last_name', 'posts', 'password', 'contact']
        write_only_fields = ['is_staff', 'first_name', 'last_name']
        extra_kwargs = {
            'is_staff': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'password': {'write_only': True},
            'contact': {'write_only': True},
        }

# accounts/serializers.py


class UserRegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=20)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 're_password', 'contact']
        extra_kwargs = {
            'password': {'write_only': True},
            're_password': {'write_only': True}
        }

    def create(self, validated_data):
        # breakpoint()
        
        if ('first_name' in validated_data and 'last_name' in validated_data):
            # user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
            user = CustomUser.objects.create_user(validated_data['email'], validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'], username = validated_data['username'], contact = validated_data['contact'])
        elif ('first_name' in validated_data and 'last_name' not in validated_data):
            user = CustomUser.objects.create_user(validated_data['email'], validated_data['password'], first_name=validated_data['first_name'], username = validated_data['username'], contact = validated_data['contact'])
        else:
            user = CustomUser.objects.create_user(validated_data['email'], validated_data['password'], username=validated_data['username'], contact = validated_data['contact'])
        return user


    def validate_email(self, value):
        if (value != '') and (bool(re.search("^[a-zA-Z0-9_.±]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$", value))):
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        # else:
        #     raise serializers.ValidationError("Enter a valid email address") # email is validated by django iteself.
        return value


    def validate_first_name(self, value):
        if value == "":
            return value
        if value.isalpha():
            return value
        raise serializers.ValidationError("First Name should only contain alphabets. Spaces, Numbers or Special Symbols are not allowed.")

    def validate_last_name(self, value):
        if value == "":
            return value
        if value.isalpha():
            return value
        raise serializers.ValidationError("Last Name should only contain alphabets. Spaces, Numbers or Special Symbols are not allowed.")


    def validate_password(self, value):
        # print(value)
        # print(self.initial_data['re_password'])
        if not bool(re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value)):
            raise serializers.ValidationError("Password must contain Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.")
        if value != self.initial_data['re_password']:
            raise serializers.ValidationError("Passwords does not match")
        return value



# def starts_with_s(value):
#     if value[0].lower() != 's':
#         breakpoint()
#         raise serializers.ValidationError("Username should start with S")
#     return value

# class UserSerializer(serializers.ModelSerializer):
    
#     def start_with_r(value):
#         if value[0].lower() != 'r':
#             raise serializers.ValidationError("Must start with r")
#         return value
    
#     # username = serializers.CharField(max_length=100, validators=[start_with_r])
    
#     postname = serializers.SlugRelatedField(many=True, read_only=True, slug_field='post_title')
#     # postname = serializers.HyperlinkedIdentityField(view_name='post-list')
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'is_staff', 'postname']

#     def validate_is_staff(self, value):
#         if value:
#             raise serializers.ValidationError('Cannot be a staff')
#         return value
    
#     def validate(self, data):
#         username = data.get('username')
#         email = data.get('email')

#         if username.lower() == 'sonia' and email.lower() != 'congress@gmail.com':
#             raise serializers.ValidationError("Cannot be other than congress")
#         return data
    

# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=100, validators=[starts_with_s])
#     email = serializers.EmailField()
#     is_staff = serializers.BooleanField()

#     def create(self, validated_data):
#         return User.objects.create(**validated_data)
    

#     def update(self, instance, validated_data):
#         print(instance.username)
#         instance.username = validated_data.get('username', instance.username)
#         print(instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.is_staff = validated_data.get('is_staff', instance.is_staff)
#         instance.save()
#         return instance
    
#     def validate_is_staff(self, value):
#         if value:
#             raise serializers.ValidationError('Cannot be a staff.')
#         return value
    
#     def validate(self, data):
#         un = data.get('username')
#         email = data.get('email')

#         if un.lower() == 'sonia' and email.lower() != 'congress@gmail.com':
#             raise serializers.ValidationError("only congress@gmail allowed")
#         return data


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()

    def create(self, valid_data):
        return CustomUser.objects.create(**valid_data)
