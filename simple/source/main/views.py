from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    template_name = 'main/index.html'


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'


class wikiPageView(TemplateView):
    template_name = 'main/wiki.html'


class quizPageView(TemplateView):
    template_name = 'main/quiz.html'


class noticePageView(TemplateView):
    template_name = 'main/notice.html'


class qnaPageView(TemplateView):
    template_name = 'main/qna.html'


class writePageView(TemplateView):
    template_name = 'main/write.html'

class postPageView(TemplateView):
    template_name = 'main/post.html'

class editPageView(TemplateView):
    template_name = 'main/edit.html'


class createPageView(TemplateView):
    template_name = 'main/create.html'