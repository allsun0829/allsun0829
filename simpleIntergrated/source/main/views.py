from django.views.generic import TemplateView
import requests
from django.shortcuts import render 
from django.conf import settings 
from isodate import parse_duration 
from django.core.paginator import Paginator # 추가된 코드
from main.models import *  

class IndexPageView(TemplateView):
    template_name = 'main/index.html'


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'


class wikiPageView(TemplateView):
    template_name = 'main/wiki.html'


#!/usr/bin/env python3
#-*- codig: utf-8 -*-
import sys
import requests
import json

def re_api(request):
    client_id = "zshypox3qz"
    client_secret = "hgu8BLJAn0fME9jV3Y7jLzBcwMnmV20KLw50RaNg"
    headers = {
        "zshypox3qz": client_id,
        "hgu8BLJAn0fME9jV3Y7jLzBcwMnmV20KLw50RaNg": client_secret,
        "Content-Type": "application/json"
    }
    language = "ko" # Language of document (ko, ja )
    model = "news" # Model used for summaries (general, news)
    tone = "2" # Converts the tone of the summarized result. (0, 1, 2, 3)
    summaryCount = "3" # This is the number of sentences for the summarized document.
    url= "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize" 
    title= "'하루 2000억' 판 커지는 간편송금 시장"
    content = "간편송금 이용금액이 하루 평균 2000억원을 넘어섰다.한국은행이 17일 발표한 '2019년 상반기중 전자지급서비스 이용 현황'에 따르면 올해 상반기 간편송금서비스 이용금액(일평균)은 지난해 하반기 대비 60.7% 증가한 2005억원으로 집계됐다. 같은 기간 이용건수(일평균)는 34.8% 늘어난 218만건이었다. 간편 송금 시장에는 선불전자지급서비스를 제공하는 전자금융업자와 금융기관 등이 참여하고 있다. 이용금액은 전자금융업자가 하루평균 1879억원, 금융기관이 126억원이었다. 한은은 카카오페이, 토스 등 간편송금 서비스를 제공하는 업체 간 경쟁이 심화되면서 이용규모가 크게 확대됐다고 분석했다. 국회 정무위원회 소속 바른미래당 유의동 의원에 따르면 카카오페이, 토스 등 선불전자지급서비스 제공업체는 지난해 마케팅 비용으로 1000억원 이상을 지출했다. 마케팅 비용 지출규모는 카카오페이가 491억원, 비바리퍼블리카(토스)가 134억원 등 순으로 많았다."
    datas = []
    data = {
        "document": {
        "title": title,
        "content" : content
        },
        "option": {
        "language": language,
        "model": model,
        "tone": tone,
        "summaryCount" : summaryCount
        }
    }
    datas.append(data)

    print(json.dumps(data, indent=4, sort_keys=True))
    response = requests.post(url, data=json.dumps(data), headers=headers)
    rescode = response.status_code
    if(rescode == 200):
        print (response.text)
    else:
        print("Error : " + response.text)
    
    context = {
        'datas' : datas
    }

    return render(request, 'main/clova_api.html', context)








def wikiPage(request): 
    # posts = []
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'main/wiki.html', context)

    # return render(request, 'main/wiki.html', {"post":posts[0]})

def wikiPost(request): 
    posts = Post.objects.all()
    context = {
            'posts' : posts
    }
    return render(request, 'main/wikiPost.html')

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

def noticePage(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 2) # 페이지네이터 함수 사용하여 2개 단위로 페이지 나누기

    page_number = request.GET.get("page") # 페이지 넘버 가져오기
    page_posts = paginator.get_page(page_number)

    return render(request, "posts/index.html", {"posts":page_posts}) # 페이지네이션 변수 page_posts를 템플릿의 posts로 받기

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

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            # location.reload()
            return redirect('/create/')
    else:
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'main/create.html', context)

