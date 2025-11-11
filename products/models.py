from django.db import models


class Category(models.Model):
    """
    Represents a product category (e.g., Electronics, Books, Clothing).
    
    Relationships:
        - One-to-Many with Product: Each category can have multiple products
    
    Fields:
        name: Unique category name
        description: Optional detailed description of the category
    """
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Category name (must be unique)"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description of this category"
    )
    
    def __str__(self):
        """Returns the category name for string representation."""
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    """
    Represents a tag/label for products (e.g., Sale, New, Popular, Premium).
    
    Relationships:
        - Many-to-Many with Product: Tags can be applied to multiple products,
          and products can have multiple tags
    
    Fields:
        name: Unique tag name
    """
    name = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Tag name (must be unique)"
    )
    
    def __str__(self):
        """Returns the tag name for string representation."""
        return self.name
    
    class Meta:
        ordering = ['name']


class Product(models.Model):
    """
    Represents a product in the catalog.
    
    Relationships:
        - Many-to-One with Category: Each product belongs to one category
        - Many-to-Many with Tag: Products can have multiple tags
    
    Fields:
        name: Product name
        description: Detailed product description (searchable)
        price: Product price with 2 decimal places
        category: Foreign key to Category model
        tags: Many-to-many relationship with Tag model
        created_at: Automatically set when product is created
        updated_at: Automatically updated when product is modified
    """
    name = models.CharField(
        max_length=200,
        help_text="Product name"
    )
    description = models.TextField(
        help_text="Detailed description of the product"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Product price (e.g., 19.99)"
    )
    
    # Foreign Key: Many-to-One relationship with Category
    # on_delete=CASCADE: When a category is deleted, delete all its products
    # related_name='products': Allows reverse lookup (category.products.all())
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products',
        help_text="Category this product belongs to"
    )
    
    # Many-to-Many: Products can have multiple tags, tags can belong to multiple products
    # blank=True: Tags are optional
    # related_name='products': Allows reverse lookup (tag.products.all())
    tags = models.ManyToManyField(
        Tag, 
        blank=True, 
        related_name='products',
        help_text="Tags associated with this product"
    )
    
    # Automatically managed timestamp fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when product was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when product was last updated"
    )
    
    def __str__(self):
        """Returns the product name for string representation."""
        return self.name
    
    class Meta:
        ordering = ['-created_at']  # Newest products first
        indexes = [
            models.Index(fields=['-created_at']),  # For sorting by date
        ]
