from django.views.generic import TemplateView
import requests
from django.shortcuts import render 
from django.conf import settings 
from isodate import parse_duration 
from .models import Post 

class IndexPageView(TemplateView):
    template_name = 'main/index.html'


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'


class wikiPageView(TemplateView):
    template_name = 'main/wiki.html'

def quizPage(request): 
    # videos = []
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_urls = 'https://www.googleapis.com/youtube/v3/videos'
    #search 
    search_params = {
        'part' : 'snippet',
        'q' : 'learn python', #query 
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 4,
        'type' : 'video' 
    }
    video_ids = []
    r = requests.get(search_url, params=search_params)
    # print(r.text)
    results = r.json()['items'] 
    for result in results: 
        video_ids.append(result['id']['videoId']) 
        
    # video 
    video_params = {
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet, contentDetails',
        'id' : ','.join(video_ids)
    }
    r = requests.get(video_urls, params=video_params)
    # print(r.text)
    results = r.json()['items'] 
    videos = []
    for result in results: 
        # print(result)
        # print(result['sinppet']['title'])
        # print(result['id'])
        # print(parse_duration(result['contentDetails']['duration']).total_seconds()/60)
        # print(result['sinppet']['thumbnails']['high']['url'])
        video_data = {
            'title' : result['snippet']['title'], 
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }', 
            'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds()/60),
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        } 
        videos.append(video_data)
    # print(videos)
    context = {
        'videos' : videos
    }
    return render(request, 'main/quiz.html', context)


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

def createPage(request): 
    forms = Post.objects.all()
    # (request.POST)
    return render(request, 'main/create.html', {'forms': forms[0]})

