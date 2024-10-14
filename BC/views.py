from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from.models import *


# Create your views here.

def Explore(request):
    return render(request, 'Explore.html')


def home(request):
    episode = Episode.objects.all()
    context = {
        'episode': episode,
    }

    return render(request, 'home.html',context=context)
    # epi = Episode.objects.all()
    # context = {
    #     'epi': epi,
    # }
    #
    # return render(request, template_name='PodCast/home.html', context=context)
