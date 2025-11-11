from django.contrib import admin
from .models import Category, Tag, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Category model.
    Customizes how categories appear in the admin panel.
    """
    list_display = ['name', 'description'] # Columns to show in the list view
    search_fields = ['name', 'description']  # Fields you search by
    ordering = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Tag model.
    Customizes how tags appear in the admin panel.
    """
    list_display = ['name']
    search_fields = ['name']  
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Product model.
    Customizes how products appear in the admin panel.
    """
    list_display = ['name', 'category', 'price', 'created_at']
    list_filter = ['category', 'tags', 'created_at']    # Filters in sidebar
    search_fields = ['name', 'description']
    filter_horizontal = ['tags']    # Better widget for many-to-many field
    ordering = ['-created_at']
    
    # Group fields in the edit form for better organization
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Make this section collapsible
        }),
    )
    
    # timestamp fields should be read-only (they're auto-generated)
    readonly_fields = ['created_at', 'updated_at']
