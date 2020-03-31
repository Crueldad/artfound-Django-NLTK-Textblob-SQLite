from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post



def home(request):
    return render(request, 'homepage/home.html')

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'homepage/home.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'homepage/home.html'

def post_detail(request, slug):
    template_name = 'homepage/home.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=True)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})