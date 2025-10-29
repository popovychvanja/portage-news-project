from django.contrib import admin
from .models import NewsArticle

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    # What columns to display in the list view
    list_display = ('title', 'pub_date', 'is_published', 'author', 'get_creator')
    list_filter = ('is_published', 'pub_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    # NEW FIELD: This field will store the ID of the user who created the article
    fields = ('title', 'excerpt', 'content', 'image', 'is_published', 'slug', 'author', 'creator')
    readonly_fields = ('creator',) # User cannot manually change the creator

    def get_creator(self, obj):
        # Helper function to display the creator's username in the list view
        return obj.creator.username if obj.creator else "N/A"
    get_creator.short_description = 'Creator'

    # 1. NEW: Override the save method to automatically set the 'creator'
    def save_model(self, request, obj, form, change):
        # If the object is new (not being changed), assign the current logged-in user as the creator
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    # 2. NEW: Override the queryset to filter based on the 'creator' field
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If the user is a superuser (admin), they see everything
        if request.user.is_superuser:
            return qs
        # If the user is staff (reporter), they only see articles they created
        return qs.filter(creator=request.user)