from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# from .models import Question

# Create your views here.
def index(request): 
    return render(request, 'apps/index.html')
def quiz(request): 
    return render(request, 'apps/quiz.html')
def notifications(request): 
    return render(request, 'apps/notifications.html')
def agora(request): 
    return render(request, 'apps/agora.html')
def write(request): 
    return render(request, 'apps/write.html')
def edit(request): 
    return render(request, 'apps/edit.html')
def post(request): 
    return render(request, 'apps/post.html')
    
# class AboutView(generic.AboutView): 
#     template_name = 'polls/about.html'
