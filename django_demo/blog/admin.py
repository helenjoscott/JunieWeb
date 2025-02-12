from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for Post model.
    Demonstrates various admin customization features.
    """
    list_display = ('title', 'author', 'status', 'created_at', 'published_at',
                   'get_tags', 'comment_count')
    list_filter = ('status', 'created_at', 'published_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('author',)
    filter_horizontal = ('tags',)
    
    def get_tags(self, obj):
        """Display tags as colored badges."""
        return format_html(
            ' '.join(f'<span style="background-color: #eee; padding: 3px; '
                    f'border-radius: 5px; margin: 2px;">{tag.name}</span>'
                    for tag in obj.tags.all())
        )
    get_tags.short_description = 'Tags'
    
    def comment_count(self, obj):
        """Display number of comments."""
        return obj.comments.count()
    comment_count.short_description = 'Comments'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content')
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('status', 'tags', 'published_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for Comment model.
    Demonstrates list display and filtering.
    """
    list_display = ('__str__', 'post', 'author', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    raw_id_fields = ('author', 'post', 'parent')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        """Custom admin action to approve multiple comments."""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated} comment{"s" if updated != 1 else ""} approved.'
        )
    approve_comments.short_description = 'Approve selected comments'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface for Tag model.
    Demonstrates basic admin configuration.
    """
    list_display = ('name', 'slug', 'post_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        """Display number of posts using this tag."""
        return obj.posts.count()
    post_count.short_description = 'Posts'