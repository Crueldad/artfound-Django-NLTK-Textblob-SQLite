from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
import sqlite3

def home(request):
    return render(request, 'homepage/home.html')


def post_detail(request):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm()
    return render(request, 'homepage/home.html', {'form': form })

# conn = sqlite3.connect('db.sqlite3')
# c = conn.cursor()


