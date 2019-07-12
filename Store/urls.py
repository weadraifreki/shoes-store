from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .Views import Shoe, Ads, Categories
# import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('shoe/', Shoe.List.as_view(), name="shoes-list"),
    path('shoe/add/', Shoe.Create.as_view(), name='shoe-create'),
    path('shoe/<int:pk>/', Shoe.Detail.as_view(), name="shoe-detail"),
    path('shoe/<int:pk>/edit/', Shoe.Edit.as_view(), name="shoe-edit"),
    path('shoe/<int:pk>/delete/', Shoe.Delete.as_view(), name="shoe-delete"),
    path('shoe/upload/', Shoe.shoe_image_upload),

    path('ads/', Ads.List.as_view(), name="ads-list"),
    path('ads/add/', Ads.Create, name="ads-add"),
    path('ads/<int:pk>/', Ads.Detail.as_view(), name="ads-detail"),
    path('ads/<int:pk>/edit/', Ads.Edit.as_view(), name="ads-edit"),
    path('ads/<int:pk>/delete/', Ads.Delete.as_view(), name="ads-delete"),
    # path('ads/<int:pk>/delete/', login_required(Ads.Delete.as_view()), name="ads-delete"),

    path('category/add/', Categories.Create.as_view(), name="category-create"),
    path('category/<int:pk>/edit/', Categories.Edit.as_view(), name="category-edit"),
    
    path('size/add/', views.SizeCreate.as_view(), name="Size-create"),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)