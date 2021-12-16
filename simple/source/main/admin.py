from django.contrib import admin
from main.models import Post, Quizz, Question, Answer, Result, BlogPost, Comment 

class PostAdmin(admin.ModelAdmin): 
    pass
admin.site.register(Post, PostAdmin)

# https://harry24k.github.io/django-week3-post/ 

admin.site.register(Quizz)
admin.site.register(Result)


class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)


admin.site.register(BlogPost)
admin.site.register(Comment)
class CommentAdmin(admin.ModelAdmin): 
    pass
# admin.site.register(Comment, CommentAdmin)