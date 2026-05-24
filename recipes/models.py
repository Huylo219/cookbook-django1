from django.db import models
from django.urls import reverse

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    ingredients = models.TextField(verbose_name='Ингредиенты')
    instructions = models.TextField(verbose_name='Приготовление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', args=[self.id])
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0
    
    def reviews_count(self):
        return self.reviews.count()

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews', verbose_name='Рецепт')
    author = models.CharField(max_length=100, verbose_name='Автор')
    rating = models.IntegerField(choices=[(i, '★' * i) for i in range(1, 6)], verbose_name='Оценка')
    comment = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author} - {self.recipe.title}'