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
def about(request): 
    return render(request, 'apps/about.html')
def products(request): 
    return render(request, 'apps/products.html')
def store(request): 
    return render(request, 'apps/store.html')
def index(request): 
    return render(request, 'apps/index.html')

# class AboutView(generic.AboutView): 
#     template_name = 'polls/about.html'
