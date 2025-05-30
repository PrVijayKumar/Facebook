from rest_framework import serializers
from testing.models import DemoTable
from datetime import datetime
import re
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
    


class TestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoTable
        fields = '__all__'
        extra_kwargs = {"email": {"error_messages": {"invalid": "Enter a valid email address."}},
                        "name": {"error_messages": {'invalid': 'Name cannot contain number or digits or special characters', 'required': 'Name cannot be blank.'}},
                        "siblings": {"error_messages": {"invalid": "siblings should be an integer and cannot be more than 10"}},
                        "dob": {"error_messages": {"invalid": "Date should have correct format. YYYY-MM-DD e.g. 2008-01-15"}},
                        "marks": {"error_messages": {"invalid": "Enter valid marks. Marks should not be greater than 100 or less than 0"}}
                        }



    def validate_name(self, value):
        # print(value)
        # print(re.search("^[a-zA-Z ]*$", value))
        if value is None:
            raise serializers.ValidationError("Name cannot be blank.")
        if not bool(re.search("^[a-zA-Z ]*$", value)):
            # print("Error")
            raise serializers.ValidationError("Name cannot contain digits or special characters.")
        return value
    
    def validate_password1(self, value):
        # print(value)
        if not bool(re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value)):
            raise serializers.ValidationError("Password must contain Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.")
        return value
    
    def validate_siblings(self, value):
        print(value)
        if value > 10:
            print("Siblings Error")
            raise serializers.ValidationError("Sibling cannot be more than 10.")
        return value
    
    def validate_marks(self, value):
        if value > 100 or value < 0:
            raise serializers.ValidationError("Marks cannot be more than 100 or less than 0")
        return value
    
    def validate_dob(self, value):
        # breakpoint()
        # dob = datetime.date(datetime.strptime(value, '%Y-%m-%d'))
        # print(datetime.now())
        # print(dob)
        # breakpoint()
        diff = value - datetime.date(datetime.today())
        # print(diff)
        if abs(diff.days//365) < 18:
            raise serializers.ValidationError("Age should be above 18 years")
        return value
    

    def validate_email(self, value):
        print(value)
        if not bool(re.search(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}", value)):
            raise serializers.ValidationError("Provide a valid email address")
        return value
    

    # def is_valid(self, *args, **kwargs):
    #     mydata = self.initial_data.copy()
    #     name = mydata.get('name')
    #     password1 = mydata.get('password1')
    #     # siblings = mydata.get('siblings')
    #     # marks = mydata.get('marks')
    #     dob = mydata.get('dob')
    #     email = mydata.get('email')
    #     mydata['name'] = self.validate_name(name)
    #     mydata['password1'] = self.validate_password1(password1)
    #     # mydata['siblings'] = self.validate_siblings(siblings)
    #     # mydata['marks'] = self.validate_marks(marks)
    #     mydata['dob'] = self.validate_dob(dob)
    #     mydata['email'] = self.validate_email(email)
    #     return super(TestingSerializer, self).is_valid(*args, **kwargs)