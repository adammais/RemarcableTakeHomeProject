from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category, Tag


def product_list(request):
    """
    Display a list of products with search and filter functionality.
    
    Supports:
    - Search by product description (case-insensitive)
    - Filter by category
    - Filter by multiple tags
    - Combining all filters together
    
    Query parameters:
    - search: Text to search in product descriptions
    - category: Category ID to filter by
    - tags: List of tag IDs to filter by
    """
    
    # Start with all products, optimized with related data
    products = Product.objects.select_related('category').prefetch_related('tags').all()
    
    # Get all categories and tags for the filter form
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Get filter parameters from URL query string
    search_query = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '')
    selected_tags = request.GET.getlist('tags')
    
    # Track active filters for display
    active_filters = {}
    
    # Search by description
    if search_query:
        # __icontains is for case-insensitive contains search
        products = products.filter(Q(description__icontains=search_query) | Q(name__icontains=search_query))
        active_filters['search'] = search_query
    
    # Filter by category
    if category_id:
        try:
            products = products.filter(category_id=category_id)
            # Get category name for display
            category = Category.objects.get(id=category_id)
            active_filters['category'] = category.name
        except (ValueError, Category.DoesNotExist):
            # Invalid category ID - ignore filter
            pass
    
    # Filter by tags (products must have all selected tags)
    if selected_tags:
        # Filter products that have all selected tags
        for tag_id in selected_tags:
            try:
                products = products.filter(tags__id=tag_id)
            except ValueError:
                # Invalid tag ID - skip this tag
                pass
        
        # Get tag names for display
        if selected_tags:
            try:
                tag_names = Tag.objects.filter(id__in=selected_tags).values_list('name', flat=True)
                active_filters['tags'] = list(tag_names)
            except ValueError:
                pass
    
    # Remove duplicates that might occur from multiple tag filters
    products = products.distinct()
    
    product_count = products.count()
    
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_tags': selected_tags,
        'active_filters': active_filters,
        'product_count': product_count,
    }
    
    return render(request, 'products/product_list.html', context)
