from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post                                          
        # fields = ['title', 'content']  
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '제목'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '내용'
                }
            )
        }

        # https://han-py.tistory.com/87