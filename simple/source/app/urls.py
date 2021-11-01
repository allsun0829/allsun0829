from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from main.views import * #IndexPageView, ChangeLanguageView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexPageView.as_view(), name='index'),

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),

    path('main/', wikiPageView.as_view(), name='wiki'),
    # path('main/quiz', quizPageView.as_view(), name='quiz'),
    path('main/quiz', quizPage, name='quiz'),
    path('main/notice', noticePageView.as_view(), name='notice'),
    path('main/qna', qnaPageView.as_view(), name='qna'),
    path('main/qna/write', writePageView.as_view(), name='write'),
    path('main/qna/post', postPageView.as_view(), name='post'),
    path('main/qna/edit', editPageView.as_view(), name='edit'),
    # path('main/create', createPageView.as_view(), name='create'),
    path('main/create', createPage, name='create'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
