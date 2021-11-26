from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post                                          
        # fields = ['title', 'content']  
        fields = '__all__'


        # https://han-py.tistory.com/87