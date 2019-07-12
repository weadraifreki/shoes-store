from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from .forms import AdForm, ShoeForm, CategoryForm, SizeForm
from .models import Shoe, Ad, Category, Picture, Size
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy, reverse
from django.utils import timezone
import random

import logging

logging.basicConfig(level=logging.DEBUG, filename='Store-app.log',\
     format='%(asctime)s - %(process)d, %(processName)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')


def index(request):
    return render(request, 'index.html', {"ads":Ad.objects.all()})

class SizeCreate(generic.edit.CreateView):
    model = Size
    success_url = reverse_lazy('index')

    def get(self, request):
        return render(request, "ُSize/create.html", {'form': SizeForm()})
    
    def post(self, request):
        form = SizeForm(request.POST)
        if form.is_valid():
            book = form.save()
            book.save()
            return HttpResponseRedirect(reverse_lazy('index'))
        return render(request, 'Size/create.html', {'form': form})


