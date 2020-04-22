from django.shortcuts import render
from .models import VisitorData


def index(request):
    return render(
        request,
        'index.html',
        context={}
    )
