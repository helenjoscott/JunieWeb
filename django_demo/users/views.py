from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm

User = get_user_model()


class SignUpView(CreateView):
    """
    View for user registration.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully. Please log in.')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    """
    View for displaying user profile.
    """
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_completion'] = self.object.get_profile_completion_percentage()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating user profile.
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying other users' profiles.
    """
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'profile_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_completion'] = self.object.get_profile_completion_percentage()
        return context