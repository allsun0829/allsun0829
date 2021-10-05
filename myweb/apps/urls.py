from django.urls import reverse
from django.urls import path, include 
from . import views

app_name = 'apps'
urlpatterns = [
    # 기본키pk는 DB 내 하나의 열 값 중복 X 
    # url마다 이름 지정 > 템플릿 변경 불필요 

    path('index.html', views.index, name="index"),
    path('quiz.html', views.quiz, name="quiz"),
    # path('about.html', views.about, name="about"),
    path('notifications.html', views.notifications, name="notifications"),
    path('agora.html', views.agora, name="agora"),
    path('write.html', views.write, name="write"),
    path('edit.html', views.edit, name="edit"),
    path('post.html', views.post, name="post"),

]