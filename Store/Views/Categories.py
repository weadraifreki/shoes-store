from ..models import Category
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView
)
from ..forms import CategoryForm
from django.urls import reverse_lazy
import logging

logging.basicConfig(level=logging.DEBUG, filename='Categories.log',\
     format='%(asctime)s - %(process)d, %(processName)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')


class Create(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('store:category-create')

    def form_valid(self, form):
        form.save()


class Edit(UpdateView):
    model = Category
    template_name = "Category/edit.html"
    success_url = "/"



