from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
#Password by default

class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels={'email':'Email'}

class EditUserProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','date_joined']

#video:78
class EditAdminProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields='__all__'
