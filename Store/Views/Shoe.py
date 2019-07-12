from ..models import Shoe, Picture
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView
)
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from ..forms import ShoeForm
import random
import logging

logging.basicConfig(level=logging.DEBUG, filename='Shoe.log',\
     format='%(asctime)s - %(process)d, %(processName)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')



class List(ListView):
    model = ShoeForm
    template_name = "Shoe/index.html"
    context_object_name = "shoes"
    paginate_by = 20
    ordering = ['-DateBuy']
    def get_queryset(self):
        return Shoe.objects.all()

class Create(CreateView):
    model = Shoe
    form_class = ShoeForm
    success_url = "/"
    template_name = "Shoe/create.html"

    def get_initial(self, *args, **kwargs):
        if "shoe_id" not in self.request.session:
            salt = random.random()
            self.request.session["salt"] = salt
            self.request.session["shoe_id"] = "NotCreatedYet" + str(salt)
    
    def form_valid(self, form):
        errors = list()
        if form.cleaned_data["code"] != "0" and len(Shoe.objects.filter(code=form.cleaned_data["code"])) == 0:
            if "shoe_id" in self.request.session and self.request.session["shoe_id"] != ("NotCreatedYet" + str(self.request.session["salt"])):
                shoe_id = self.request.session["shoe_id"]
                form.instance.id = shoe_id
                form.save()
                del self.request.session["salt"]
                del self.request.session["shoe_id"]
                self.request.session.modified = True
                return HttpResponseRedirect(reverse_lazy("store:shoe-detail", kwargs={"pk":shoe_id}))
            else:
                errors.append("امکان ایجاد کفش بدون عکس وجود ندارد.")
        else:
            errors.append("کد کفش تکراری می باشد.")
        
        return render(self.request, "Shoe/create.html", {"form": form, "errors": errors})

    def form_invalid(self, form):
        errors = "مقادیر وارد شده صحیح نمی باشد."
        return render(self.request, "Shoe/create.html", {"form": form, "errors": errors})

class Detail(DetailView):
    model = Shoe
    template_name = "Shoe/detail.html"
    def get_queryset(self):
        return Shoe.objects.filter(is_active=True)

class Edit(UpdateView):
    model = Shoe
    template_name = "Shoe/edit.html"
    success_url = reverse_lazy("store:shoes-list")

class Delete(DeleteView):
    model = Shoe
    template_name = "Shoe/delete.html"
    success_url = reverse_lazy('store:shoes-list')


def create_blank_shoe_record():
    try:
        shoe = Shoe.objects.create(code=0, price_sell=0, price_buy=0, number_buy=0, number_left=0)
        return shoe.id
    except Exception as err:
        print(err)
        return -1

def shoe_image_upload(request):
    data = {"result": False}
    if request.method == 'POST' and request.FILES['myfile'] \
        and "salt" in request.session and "shoe_id" in request.session:
        if request.session["shoe_id"] == "NotCreatedYet" + str(request.session["salt"]):
            # create new shoe record
            shoe_id = create_blank_shoe_record()
            request.session["shoe_id"] = shoe_id
        else:
            shoe_id = request.session["shoe_id"]

        myfile = request.FILES['myfile']
        picture = Picture.objects.create(image=myfile, shoe_id=shoe_id)

        data["result"] = True
        data["name"] = myfile.name
        data["shoe_id"] = shoe_id
    return JsonResponse(data)
