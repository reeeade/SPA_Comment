from django import forms
from .models import Comment, User
from captcha.fields import CaptchaField


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'homepage']


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['text', 'parent', 'captcha']
        widgets = {
            'parent': forms.HiddenInput(),
        }
