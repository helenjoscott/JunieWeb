from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post URLs
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Tag URLs
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
]