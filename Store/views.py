from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .forms import AdForm, ShoeForm, CategoryForm, SizeForm
from .models import Shoe, Ad, Category, Picture, Size
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy, reverse
from django.utils import timezone
import random

import logging

logging.basicConfig(level=logging.DEBUG, filename='application.log',\
     format='%(asctime)s - %(process)d, %(processName)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')


def index(request):
    return render(request, 'index.html', {"ads":Ad.objects.all()})


class ShoesList(generic.ListView):
    model = Shoe
    template_name = "Shoe/index.html"
    context_object_name = "shoes"
    paginate_by = 20
    ordering = ['-DateBuy']
    def get_queryset(self):
        return Shoe.objects.all()

class ShoeCreate(generic.edit.FormView):
    def get(self, request):
        salt = random.random()
        request.session["salt"] = salt
        request.session["shoe_id"] = "NotCreatedYet" + str(salt)
        last_id = Shoe.objects.latest('id').id
        form = ShoeForm(initial={'Id': last_id})
        return render(request, "Shoe/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        errors = []
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            if form.cleaned_data["Code"] != "0" and len(Shoe.objects.filter(Code=form.cleaned_data["Code"])) == 0:
                if "shoe_id" in request.session \
                    and request.session["shoe_id"] == form.cleaned_data["id"]:
                    shoe = form.save()
                    shoe.save()
                    del request.session["salt"]
                    del request.session["shoe_id"]
                    return render(request, 'index')
                else:
                    return HttpResponseRedirect(reverse_lazy('shoe-create'))
            else:
                errors.append("کد کفش تکراری می باشد.")
        else:
            errors.append("مقادیر وارد شده صحیح نمی باشد.")
        logging.warning('get error in validation')
        return render(request, "Shoe/create.html", {"form": form, "errors": errors})

class shoeEdit(generic.edit.UpdateView):
    model = Shoe
    template_name = "Shoe/edit.html"
    success_url = "/"


class AdsList(generic.ListView):
    template_name = "Ads/index.html"
    context_object_name = 'ads'
    paginate_by = 20
    ordering = ['-DatePublish']

    def get_queryset(self):
        return Ad.objects.all()

class AdDetail(generic.DetailView):
    model = Ad
    template_name = "Ads/detail.html"
    def get_queryset(self):
        return Ad.objects.filter(DatePublish__lte=timezone.now(), DateExpire__gte=timezone.now())

class AdDelete(generic.DeleteView):
    model = Ad
    template_name = "Ads/delete.html"
    success_url = reverse_lazy('index')
    # def get_queryset(self):
    #         pass

class AdEdit(generic.edit.UpdateView):
    model = Ad
    template_name = "Ads/edit.html"
    success_url = "/"


class CategoryCreate(generic.edit.CreateView):
    model = Category

    success_url = reverse_lazy('index')

    # def get_success_url(self):
    #         return self.object.account_activated_url()

    # def get_form_class(self):
    #         if self.request.user.is_staff:
    #                 return AdminAccountForm
    #         return AccountForm

    # def get_form_kwargs(self):
    #         kwargs = super(AccountCreateView, self).get_form_kwargs()
    #         kwargs['owner'] = self.request.user
    #         return kwargs

    # def form_valid(self, form):
    #         send_activation_email(self.request.user)
    #         return super(AccountCreateView, self).form_valid(form)

    def get(self, request):
        return render(request, "Category/create.html", {'form': CategoryForm()})
    
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            book = form.save()
            book.save()
            return HttpResponseRedirect(reverse_lazy('index'))
        return render(request, 'Category/create.html', {'form': form})

class CategoryEdit(generic.edit.UpdateView):
    model = Category
    template_name = "Category/edit.html"
    success_url = "/"


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



# @login_required(login_url='/login/')
def adsCreate(request):
    errors = []
    try:
        if request.method == "GET":
            form = AdForm()
            # return render(request, "Ads/Create.html", {"form": form})
        else:
            form = AdForm(request.POST)
            # vahid = request.POST["Code"]
            # print(vahid)
            if form.is_valid():
                ad = Ad()
                if len(Ad.objects.filter(Code=form.cleaned_data["Code"])) == 0:
                    ad.Code = form.cleaned_data["Code"]
                    ad.Price = form.cleaned_data["Price"]
                    ad.Title = form.cleaned_data["Title"]
                    ad.save()
                else:
                    # vahid = Ads.objects.get(Code=form.cleaned_data["Code"])
                    # print(vahid)
                    # for item in vahid:
                    #         print(item)
                    # print("code is repeated")
                    return render(request, "Ads/Create.html", {"form": form, "errors":{"code problem":1}})
            # post = form.save(commit=False)
            # post.save()
            else:
                errors.append("Ad Code is repeated.")
    except Exception as e:
        print("error occur", str(e))
        errors.append("Unkown error occur, please try again!")
    return render(request, "Ads/Create.html", {"form": form, "errors":errors})

def create_blank_shoe_record():
    try:
        shoe = Shoe.objects.create(code=0, price_sell=0, price_buy=0, number_buy=0, number_left=0)
        # shoe = Shoe()
        # shoe.Code = 0
        # shoe.PriceSell = 0
        # shoe.PriceBuy = 0
        # shoe.Name = ""
        # shoe.NumberBuy = 0
        # shoe.NumberLeft = 0
        # shoe.save()
        return shoe.id
    except Exception as err:
        print(err)
        return -1

def update_shoe_record(shoe):
    shoe = Shoe.objects.get(id=shoe["Id"])
    shoe.Code = shoe["Code"]
    shoe.PriceSell = shoe["PriceSell"]
    shoe.PriceBuy = shoe["PriceBuy"]
    shoe.Name = shoe["Name"]
    shoe.NumberBuy = shoe["NumberBuy"]
    shoe.NumberLeft = shoe["NumberLeft"]
    shoe.save()


def simple_upload(request):
    data = {"result": False}
    if request.method == 'POST' and request.FILES['myfile'] \
        and "salt" in request.session and "shoe_id" in request.session:
        if request.session["shoe_id"] == "NotCreatedYet" + request.session["salt"]:
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
