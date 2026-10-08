from django.contrib import admin

from .models import Category, Comment, Product, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for categories; the slug is filled from the name."""

    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for products, filterable by category and tags."""

    list_display = (
        "name",
        "category",
        "price",
        "average_rating",
        "rating_count",
        "created_at",
    )
    list_select_related = ("category",)
    list_filter = ("category", "tags")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for comments, searchable by author and text."""

    list_display = ("product", "user", "guest_name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("guest_name", "guest_email", "text", "user__username")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for tags, searchable by name."""

    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
