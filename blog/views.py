from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog,BlogAuthor,BlogComment
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from .forms import CommentCreateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

def index(request):
    num_blogs=Blog.objects.all().count()
    num_authors=BlogAuthor.objects.all().count()

    num_visits=request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1

    context={
        'num_blogs':num_blogs,
        'num_authors':num_authors,
        'num_visits':num_visits
    }
    return render(request,'index.html',context)

class BlogListView(generic.ListView):
    model = Blog

class BlogDetailView(generic.DetailView):
    model = Blog

    def get_context_data(self,**kwargs):
        context=super(BlogDetailView,self).get_context_data(**kwargs)

        blogcomments=BlogComment.objects.all().filter(blog__exact=self.kwargs['pk'])

        context['comments']=blogcomments
        return  context

class BlogAuthorListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 2

class BlogAuthorDetailView(generic.DetailView):
    model = BlogAuthor

    def get_context_data(self, **kwargs):
        context=super(BlogAuthorDetailView, self).get_context_data(**kwargs)
        blogs=Blog.objects.filter(author__exact=self.kwargs['pk'])
        context['blogs']=blogs

        return context

@login_required
def create_comment_blog(request,pk):
    blog=get_object_or_404(Blog,pk=pk)
    if request.method=='POST':
        form=CommentCreateForm(request.POST)

        if form.is_valid():
            comment=BlogComment(blog=blog,description=form.cleaned_data['description'])
            comment.save()
            return HttpResponseRedirect(reverse('blog-detail',kwargs={'pk':pk}))
    else:
        form=CommentCreateForm()

    context={
        'form':form,
        'blog':blog
    }

    return render(request,'blog/create_comment_blog.html',context=context)

class CreateBlogComment(LoginRequiredMixin,CreateView):
    model = BlogComment
    fields = ['description']

    def get_context_data(self, **kwargs):
        context=super(CreateBlogComment, self).get_context_data(**kwargs)
        context['blog']=get_object_or_404(Blog,pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super(CreateBlogComment,self).form_valid(form)

    def get_success_url(self):

        return reverse('blog-detail',kwargs={'pk':self.kwargs['pk'],})