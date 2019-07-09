from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
# import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('shoe/', views.ShoesList.as_view(), name="shoes-list"),
    path('shoe/add/', views.ShoeCreate.as_view(), name='shoe-create'),
    path('shoe/<int:pk>/', views.AdDetail.as_view(), name="shoe-detail"),
    path('shoe/<int:pk>/delete/', views.AdDelete.as_view(), name="shoe-delete"),
    path('shoe/<int:pk>/edit/', views.AdDelete.as_view(), name="shoe-edit"),
    path('shoe/upload/', views.simple_upload),

    path('ads/', views.AdsList.as_view(), name="ads-list"),
    path('ads/add/', views.adsCreate, name="ads-add"),
    path('ads/<int:pk>/', views.AdDetail.as_view(), name="ads-detail"),
    path('ads/<int:pk>/delete/', views.AdDelete.as_view(), name="ads-delete"),
    path('ads/<int:pk>/edit/', views.AdDelete.as_view(), name="ads-edit"),
    # path('ads/<int:pk>/delete/', login_required(views.AdDelete.as_view()), name="ads-delete"),

    path('category/add/', views.CategoryCreate.as_view(), name="category-create"),
    path('category/<int:pk>/edit/', views.CategoryEdit.as_view(), name="category-edit"),
    
    path('size/add/', views.CategoryCreate.as_view(), name="Size-create"),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)