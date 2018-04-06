from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForms
from .models import Article


# Create your views here.
def index(request):
    article_list = Article.objects.query_by_time()
    loginform = LoginForms()
    return render(request, 'cmsapp/index.html', {'loginform': loginform, 'article_list': article_list})
