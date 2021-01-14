from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/<int:pk>/<slug:slug>', PostDetail.as_view(), name='detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('post-update/<int:pk>/<slug:slug>', PostUpdateView.as_view(), name='post_update'),
    path('post-delete/<int:pk>/<slug:slug>', DeletePostView.as_view(), name="post_delete"),
    path('category/<int:pk>/<slug:slug>', CategoryDetail.as_view(), name='category-detail'),
    path('tag/<slug:slug>', TagDetail.as_view(), name='tag_detail'),
    path('create-post', PostCreationView.as_view(), name='create-post'),
]
