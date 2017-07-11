from django.shortcuts import render
from django.http import HttpResponse
from djatex import render_latex

# Create your views here.

def index(request):
    context = {'author': b'Joe Blow', 'title': b'An old result'}
    return render_latex('testfile.pdf', 'testapp/test.tex', context=context)
