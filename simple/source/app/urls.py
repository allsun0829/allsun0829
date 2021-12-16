from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from main.views import * #IndexPageView, ChangeLanguageView

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('', IndexPageView.as_view(), name='index'),
    path('', index, name='index'),

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),

    path('main/', wikiPage, name='wiki'),
    path('main/wikiCreate/', create, name='wikiCreate'),
    path('main/wikiPost/<int:post_id>/', wikiPost, name='wikiPost'),
    path('main/wikiPost/<int:post_id>/wikiUpdate', wikiUpdate, name='wikiUpdate'),
    # path('main/wikiPost/<int:post_id>/wikiUpdate', edit, name='wikiUpdate'),
    path('main/wikiDelete/<int:pk>/', delete, name='wikiDelete'),

    path('main/relativeVideos', relativeVideos, name='relativeVideos'),
    # path('main/quiz/', quizPage, name='quiz'),
    # path('main/quiz/<int:quiz_id>/', quizDetail, name='quizDetail'),
    path('main/quiz/', QuizListView.as_view(), name='quiz'),
    path('main/quiz/<int:pk>/', quiz_view, name='quizDetail'),
    path('<pk>/save/', save_quiz_view, name='saveData'),
    path('<pk>/data/', quiz_data_view, name='quizData'),


    # path('main/notice', noticePageView.as_view(), name='notice'),
    path('main/notice/', post_list, name='notice'),
    path('main/write/', post_write, name='post_write'),
    path('main/detail/<int:bpost_id>/', post_detail, name='post_detail'),
    path('main/detail/<int:bpost_id>/comment', comment_write, name='comment_write'),
    path('main/detail/<int:bpost_id>/update', post_update, name='post_update'),
    path('main/delete/<int:pk>/', post_delete, name='post_delete'),

    path('main/qna', qnaPageView.as_view(), name='qna'),
    # path('main/qna/write', writePageView.as_view(), name='write'),
    # path('main/qna/post', postPageView.as_view(), name='post'),
    # path('main/qna/edit', editPageView.as_view(), name='edit'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
