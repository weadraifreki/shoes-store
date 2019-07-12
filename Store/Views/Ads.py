from ..models import Ad
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView
)
from ..forms import AdForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

import logging

logging.basicConfig(level=logging.DEBUG, filename='Ads.log',\
     format='%(asctime)s - %(process)d, %(processName)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')


class List(ListView):
    template_name = "Ads/index.html"
    context_object_name = 'ads'
    paginate_by = 20
    ordering = ['-DatePublish']

    def get_queryset(self):
        return Ad.objects.all()


class Create(CreateView):
    template_name = "Ads/create.html"
    form_class = AdForm

    def form_valid(self, form):
        if len(Ad.objects.filter(Code=form.cleaned_data["Code"])) == 0:
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy("store:ads-detail", kwargs={"pk":obj.id}))
        else:
            return render(request, "Ads/Create.html", {"form": form, "errors":{"code problem":"کد تکراری می باشد"}})


class Detail(DetailView):
    model = Ad
    template_name = "Ads/detail.html"
    def get_queryset(self):
        return Ad.objects.filter(DatePublish__lte=timezone.now(), DateExpire__gte=timezone.now())


class Delete(DeleteView):
    model = Ad
    template_name = "Ads/delete.html"
    success_url = reverse_lazy('store:ads-list')


class Edit(UpdateView):
    model = Ad
    template_name = "Ads/edit.html"
    success_url = reverse_lazy("store:ads-list")

