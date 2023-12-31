
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from.models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    post=Post.objects.all()
    return render(request,"webapp/home.html",{"posts":post})

class PostListView(ListView):
    model = Post
    template_name = 'webapp/home.html'
    context_object_name = 'posts'
    ordering =['-date_posted']
    paginate_by =3

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields =['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields =['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url='/'
    
    def test_func(self):
        post = self.get_object()
        print("POST",post)
        if self.request.user == post.author:
            return True
        return False

class UserPostListView(ListView):
    model = Post
    template_name = 'webapp/user_posts.html'
    context_object_name = 'posts'
    paginate_by =3

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))# WE ARE GETTING USERNAME FROM URL AND SENDING TO USER MODEL AND CHECKING  
        return Post.objects.filter(author=user).order_by('-date_posted') #GETTING THAT USER AND FILTERING THE POSTS FOR THAT AUTHOR


def about(request):
    return render(request,'webapp/about.html',{'title':'About'})
