from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import sqlite3


def textanalysis(request):
    return render(request, 'textanalysis/textanalysis.html')
