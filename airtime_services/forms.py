from accounts.models import Profile
from django import forms
from django.contrib.auth.forms import  UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, required=True, help_text='Required. Inform a valid email address.')
    

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

        
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no','address','state')