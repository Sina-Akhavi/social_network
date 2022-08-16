from django.shortcuts import render
from django.views import View
from .models import Post

# Create your views here.
class HomePage(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/home_page.html', context={'posts': posts})
