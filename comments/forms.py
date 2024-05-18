from django import forms
from django.core.exceptions import ValidationError
from .models import Comment, User
from captcha.fields import CaptchaField
from PIL import Image


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'homepage']


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['text', 'parent', 'image', 'file', 'captcha']
        widgets = {
            'parent': forms.HiddenInput(),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 500 * 1024:
                raise ValidationError("Размер файла изображения не должен превышать 500 Кб.")

            img = Image.open(image)
            if img.format not in ['JPEG', 'JPG', 'GIF', 'PNG']:
                raise ValidationError("Допустимы только изображения форматов JPG, GIF, PNG.")

            max_width, max_height = 320, 240
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                img.save(image.file, format=img.format)

        return image

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 100 * 1024:
                raise ValidationError("Размер текстового файла не должен превышать 100 Кб.")
            if not file.name.endswith('.txt'):
                raise ValidationError("Допустимы только текстовые файлы формата .txt.")
        return file
