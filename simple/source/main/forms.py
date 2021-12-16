from django import forms
from .models import Post, BlogPost, Comment 

class PostForm(forms.ModelForm):
    class Meta:
        model = Post                                          
        fields = ['category','title', 'body']  
        # fields = '__all__'
        widgets = {
            'category': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '분류'
                }
            ),
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

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': '여기에 댓글 달기 ...',
        'rows': '4',
    }))
    class Meta:
        model = Comment
        fields = ('body', )