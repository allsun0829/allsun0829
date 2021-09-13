from django.urls import path 
from . import views

app_name = 'polls'
urlpatterns = [
    # url마다 이름 지정 > 템플릿 변경 불필요 
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]