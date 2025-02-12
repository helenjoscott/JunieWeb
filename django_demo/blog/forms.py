from django import forms
from .models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.
    Demonstrates form validation and widget customization.
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'featured_image', 'status', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }
    
    def clean_title(self):
        """Custom validation for title field."""
        title = self.cleaned_data['title']
        if len(title.split()) < 3:
            raise forms.ValidationError(
                "Title must contain at least three words."
            )
        return title
    
    def clean(self):
        """Custom validation involving multiple fields."""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        content = cleaned_data.get('content')
        
        if status == 'published' and len(content) < 100:
            raise forms.ValidationError(
                "Published posts must have at least 100 characters."
            )
        return cleaned_data


class CommentForm(forms.ModelForm):
    """
    Form for submitting comments.
    Demonstrates form inheritance and custom widgets.
    """
    parent = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        required=False,
        widget=forms.HiddenInput
    )
    
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }
    
    def clean_content(self):
        """Custom validation for comment content."""
        content = self.cleaned_data['content']
        if len(content.strip()) < 10:
            raise forms.ValidationError(
                "Comment must be at least 10 characters long."
            )
        return content


class TagForm(forms.ModelForm):
    """
    Form for creating and editing tags.
    Demonstrates simple form configuration.
    """
    class Meta:
        model = Tag
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }