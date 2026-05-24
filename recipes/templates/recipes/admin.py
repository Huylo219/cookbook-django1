from django.contrib import admin
from .models import Recipe, Review

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'reviews_count')
    search_fields = ('title',)
    
    def reviews_count(self, obj):
        """Подсчет количества отзывов"""
        return obj.reviews_count()
    
    reviews_count.short_description = 'Кол-во отзывов'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('author', 'comment')