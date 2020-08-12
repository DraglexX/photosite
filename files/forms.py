from django import forms
from photosite.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'album_id', 'image')
