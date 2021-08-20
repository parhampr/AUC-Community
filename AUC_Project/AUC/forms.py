from django import forms
from .models import Profile
import re
from .models import getImage, random_img


class UserRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if not (args or kwargs):
            random_img()
        super(UserRegisterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password', 'profile_pic', 'private']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': 'autofocus',
                'placeholder': 'Mark Xhentti',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Elon',
            }),
            'profile_pic': forms.FileInput(attrs={
                'id': 'userfile',
                'style': 'display: none;'
            }),
            'private': forms.CheckboxInput(attrs={
                'class': 'form-check-input m-0',
                'id': 'PrivateSwitch',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'xMark_eloN',
                'class': 'form-control',
                'autocomplete': 'username',
                'spellcheck': 'false'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'required': 'required',
                'autocomplete': 'current-password'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Elon@Musk.com',
                'class': 'form-control',
                'autocomplete': 'email',
                'spellcheck': 'false',
                'required': 'required'
            })
        }

    def clean(self):
        cd = super(UserRegisterForm, self).clean()
        password1 = cd.get('password')
        if Profile.objects.filter(email=cd.get('email')).exists():
            raise forms.ValidationError(
                "The email provided already exists <br> <span style='color: var(--color-common)'>Please Login to Continue</span>")
        elif re.search('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$', password1) is None:
            raise forms.ValidationError(
                "Invalid Password Sequence")

        return cd

    def getImageURL(self):
        return f'AUC/images/{getImage()}'