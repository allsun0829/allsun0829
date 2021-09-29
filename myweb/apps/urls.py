from django.urls import reverse
from django.urls import path, include 
from . import views

app_name = 'apps'
urlpatterns = [
    # 기본키pk는 DB 내 하나의 열 값 중복 X 
    # url마다 이름 지정 > 템플릿 변경 불필요 

    path('index', views.index),
    path('about', views.about),
    # path(r'About/$', views.about, name='about'), 
    # path('', views.AboutView.as_view(), name='about'), 
    # path('about.html', views.about),
    path('products', views.products),
    path('store', views.store),
]