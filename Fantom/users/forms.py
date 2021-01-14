from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from users.models import UserProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.field_class = 'mt-10'

        self.helper.layout = Layout(
            # Field('user', css_class='form-control', ),
            Field('birthday', css_class='single-input', ),
            Field('bio', css_class='form-control', ),
            Field('image', css_class='form-control', ),
        )
        self.helper.add_input(Submit('submit', 'Save', css_class='generic-btn submit-btn success-border medium'))

    class Meta:

        model = UserProfile
        fields = ('birthday', 'bio', 'image')
        widgets = {
            'birthday':forms.DateInput(attrs={"type": 'date'})
        }

