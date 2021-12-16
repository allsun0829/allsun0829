from django.views.generic import TemplateView, ListView
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings 
from isodate import parse_duration 
from django.core.paginator import Paginator # 추가된 코드
from main.models import Post, Quizz, Question, Answer, Result, BlogPost, Comment  
from main.forms import * 
from django.urls import path, re_path, reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import QuizSerializer
import random
from django.http import JsonResponse 
from gensim.summarization.summarizer import summarize 

# class IndexPageView(TemplateView):
#     template_name = 'main/index.html'
def index(request):
    return render(request, 'main/index.html')

class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'

def wikiPage(request): 
    posts = Post.objects.order_by('-created_at') #.all() 
    context = {
        'posts' : posts
    }
    return render(request, 'main/wiki.html', context)

def wikiPost(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    body_summary = summarize(post.body, ratio=0.25)
    context ={ 
        # 'post' : post, 
        'post_id': post.post_id, 
        'category': post.category, 
        'title': post.title,
        'body': post.body,
        'created_at': post.created_at, 
        'updated_at': post.updated_at, 
        'body_summary' : body_summary,
    }
    return render(request, 'main/wikiPost.html', context)

#punctuation_text = (post.body).replace("니다", "니다.") #습니다. 입니다.
#summarize()
    
def wikiUpdate(request, post_id): 
    post = Post.objects.get(post_id=post_id)
    form = PostForm(instance=post) 

    if request.method == 'POST':
        print(request.POST)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('/main/wikiPost/'+str(post.pk))

    context = { 'form' : form }
    return render(request, 'main/wikiUpdate.html', context)

def create(request):
    if request.method == 'POST':
        print(request.POST)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('/main/')
    else:
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'main/wikiCreate.html', context)

def edit(request, post_id):
    post = Post.objects.get(post_id=post_id)

    # 글을 수정 후 제출 
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            # post.post_id = form.cleaned_data['post_id']
            post.category = form.cleaned_data['category']
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            # post.created_at = form.cleaned_data['created_at']
            post.save()
            return redirect('/main/wikiPost/'+str(post.pk))

    # 수정 위해 페이지에 접속 
    else:
        form = PostForm()
        context={
            'form':form,
            'writing':True,
            'now':'edit',
        }
        return render(request, 'main/wikiUpdate.html',context)
    # https://ssungkang.tistory.com/entry/django-17-%EA%B8%80-%EC%82%AD%EC%A0%9C-%EB%B0%8F-%EC%88%98%EC%A0%95-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0?category=320582

def delete(request, pk): 
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('/main/')
    context={'post':post}
    return render(request, 'main/wikiDelete.html', context)

# @api_view(['GET']) #주어진 개수만큼 랜덤한 퀴즈를 반환
# def randomQuiz(request, quiz_id):
#     totalQuizs = Quiz.objects.all()
#     randomQuizs = random.sample(list(totalQuizs), quiz_id)
#     serializer = QuizSerializer(randomQuizs, many=True)
#     return Response(serializer.data)
class QuizListView(ListView): 
    model = Quizz
    template_name='main/quiz.html'

def quiz_view(request, pk): 
    quiz =  Quizz.objects.get(pk=pk)
    return render(request, 'main/quizDetail.html', {'obj': quiz})

def quiz_data_view(request, pk): 
    quiz =  Quizz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions(): 
        answers = []
        for a in q.get_answers(): 
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({'data': questions, 'time': quiz.time, })

def save_quiz_view(request, pk): 
    if request.is_ajax(): 
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        # print(type(data_))
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys(): 
            print('key: ', k)
            question = Question.objects.get(text=k) 
            questions.append(question)
        user = request.user 
        quiz = Quizz.objects.get(pk=pk)
        score = 0 
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None 

        for q in questions: 
            a_selected = request.POST.get(q.text)

            if a_selected != "": 
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers: 
                    if a_selected == a.text: 
                        if a.correct: 
                            scroe += 1 
                            correct_answer = a.text
                    else:  
                        if a.correct: 
                            correct_answer = a.text
                results.append({str(q):{'correct_answer':correct_answer, 'answered': a_selected}})
            else: 
                results.append({str(q): 'not_answered'}) 
        score_ = score * multiplier 
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass: 
            return JsonResponse({'passed': True, 'score': score_, 'results': results }) 
        else: 
            return JsonResponse({'passed': False, 'score': score_, 'results': results }) 

def quizPage(request): 
    quizs = Quiz.objects.all()
    context = {
        'quizs' : quizs
    }
    return render(request, 'main/quiz.html', context)

def quizDetail(request, quiz_id): 
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    randomQuizs = random.sample(list(quizs), quiz_id)
    serializer = QuizSerializer(randomQuizs, many=True)
    return render(request, 'main/quizDetail.html')

def relativeVideos(request): 
    # videos = []
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_urls = 'https://www.googleapis.com/youtube/v3/videos'
    #search 
    search_params = {
        'part' : 'snippet',
        'q' : 'learn python', #query
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 8,
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
    return render(request, 'main/relativeVideos.html', context)



class noticePageView(TemplateView):
    template_name = 'main/notice.html'

def noticePage(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 2) # 페이지네이터 함수 사용하여 2개 단위로 페이지 나누기

    page_number = request.GET.get("page") # 페이지 넘버 가져오기
    page_posts = paginator.get_page(page_number)

    return render(request, "posts/index.html", {"posts":page_posts}) # 페이지네이션 변수 page_posts를 템플릿의 posts로 받기

# @login_required
def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()
        # if not title:
        #     errors.append('제목을 입력하세요.')
        # if not body:
        #     errors.append('내용을 입력하세요.')
        # if not errors:
        post = BlogPost.objects.create(user=request.user, title = title, body = body)
        return redirect(reverse('post_detail', kwargs={'bpost_id': post.bpost_id}))
    return render(request, 'main/write.html', {'user':request.user, 'errors':errors})

def post_list(request):
    posts = BlogPost.objects.order_by('-created_at')
    return render(request, 'main/notice.html', context = {'posts':posts})

def post_detail(request, bpost_id):
    post = get_object_or_404(BlogPost, pk = bpost_id)
    comments = Comment.objects.filter(post=post.bpost_id)
    return render(request, 'main/detail.html', context = {'post':post, 'comments':comments})

def comment_write(request, bpost_id):
    errors =[]
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, pk = bpost_id)
        post_id = post.bpost_id
        # post_id = request.POST.get('post_id','').strip()
        body = request.POST.get('body', '').strip()
        
        # if not body:
        #     errors.append("댓글을 입력하세요.")
        # if not errors:
        comment = Comment.objects.create(user = request.user, post_id = post_id, body = body)
        return redirect(reverse('post_detail', kwargs = {'post_id':comment.post_id}))
            
    return render(request, 'main/comment.html', {'user':request.user}) #, 'errors':errors

def post_update(request, bpost_id): 
    post = BlogPost.objects.get(post_id=post_id)
    # form = PostForm(instance=post) 

    # if request.method == 'POST':
    #     print(request.POST)
    #     form = PostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         post = form.save()
    #         return redirect('/main/wikiPost/'+str(post.pk))

    # context = { 'form' : form }

    # form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        print(form.cleaned_data)
        # post.post_id = form.cleaned_data['post_id']
        # post.category = form.cleaned_data['category']
        post.title = form.cleaned_data['title']
        post.body = form.cleaned_data['body']
        # post.created_at = form.cleaned_data['created_at']
        post.save()
        return redirect('/main/detail/'+str(post.pk))

    # 수정 위해 페이지에 접속 
    else:
        form = PostForm()
        context={
            'form':form,
            'writing':True,
            'now':'edit',
        }
        return render(request, 'main/update.html',context)
    return render(request, 'main/update.html', context)

def post_delete(request, pk): 
    post = BlogPost.objects.get(pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('/main/notice/')
    context={'post':post}
    return render(request, 'main/delete.html', context)
    
class qnaPageView(TemplateView):
    template_name = 'main/qna.html'


class writePageView(TemplateView):
    template_name = 'main/write.html'

class postPageView(TemplateView):
    template_name = 'main/post.html'

class editPageView(TemplateView):
    template_name = 'main/edit.html'



# def createPage(request): 
#     forms = Post.objects.all()
#     # (request.POST)
#     return render(request, 'main/create.html', {'forms': forms[0]})

