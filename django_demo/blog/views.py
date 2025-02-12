from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm, TagForm


class PostListView(ListView):
    """
    Display list of published blog posts.
    Demonstrates queryset manipulation and pagination.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        search_query = self.request.GET.get('search')
        tag_slug = self.request.GET.get('tag')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        return queryset.select_related('author').prefetch_related('tags')


class PostDetailView(DetailView):
    """
    Display a single blog post.
    Demonstrates template rendering and form handling.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(
            parent=None,
            is_approved=True
        ).select_related('author')
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        
        return redirect(self.object.get_absolute_url())


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new blog post.
    Demonstrates form processing and file uploads.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == 'published':
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing blog post.
    Demonstrates permission checking and form handling.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        if form.instance.status == 'published' and not form.instance.published_at:
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post.
    Demonstrates permission checking and deletion confirmation.
    """
    model = Post
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_confirm_delete.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


class TagListView(ListView):
    """
    Display list of all tags.
    Demonstrates basic list view functionality.
    """
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'


class TagDetailView(DetailView):
    """
    Display posts for a specific tag.
    Demonstrates relationship traversal.
    """
    model = Tag
    template_name = 'blog/tag_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.filter(
            status='published'
        ).select_related('author')
        return context