from django import forms
from django.utils import timezone
from django.contrib.admin import widgets
from datetime import datetime
from .models import Category, Size, AdSize

class AdForm(forms.Form):
    Code = forms.CharField(label="کد آگهی", max_length=100, required=True)
    Title = forms.CharField(label="عنوان آگهی", max_length=300, required=True)
    Price = forms.FloatField(label="قیمت", min_value=0, required=True)
    Off = forms.IntegerField(label="میزان تخفیف به ریال", min_value=0, required=True)
    # DateRegister = forms.DateTimeField(label="تاریخ ثبت آگهی", required=True)
    DatePublish = forms.DateTimeField(label="تاریخ انتشار آگهی",input_formats=['%Y-%m-%d %H:%M:%S'], initial=datetime.now)
    # DatePublish = forms.DateTimeField(label="تاریخ انتشار آگهی", required=True)
    DateExpire = forms.DateTimeField(label="تاریخ انقضای آگهی", input_formats=['%Y-%m-%d %H:%M:%S'], initial=datetime.now)#  widget=forms.widgets.DateTimeInput(format="%d/%m/%Y %H:%M:%S", attrs={'placeholder':"DD/MM/YY HH:MM:SS"}), required=True)
    IsSpecial = forms.BooleanField(label="آگهی ویژه")
    Description = forms.CharField(label="توضیحات", widget=forms.Textarea)

class ShoeForm(forms.Form):
    Id = forms.IntegerField(widget=forms.HiddenInput())
    Code = forms.CharField(max_length=100)
    Name = forms.CharField(max_length=250)
    PriceSell = forms.FloatField(min_value=0)
    PriceBuy = forms.FloatField(min_value=0)
    DateBuy = forms.DateTimeField(label="تاریخ خرید",input_formats=['%Y-%m-%d %H:%M:%S'], initial=datetime.now)
    # IsDeleted = forms.BooleanField()
    IsActive = forms.BooleanField()
    NumberBuy = forms.IntegerField(min_value=0,)
    NumberLeft = forms.IntegerField(min_value=0,)
    # Images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)

class SizeForm(forms.ModelForm):

    class Meta:
        model = Size
        fields = ('size_number', )

