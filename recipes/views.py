from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Recipe, Review
from .forms import ReviewForm, RecipeForm

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', {'recipes': recipes})

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = Recipe.objects.create(
                title=form.cleaned_data['title'],
                ingredients=form.cleaned_data['ingredients'],
                instructions=form.cleaned_data['instructions']
            )
            messages.success(request, 'Рецепт успешно добавлен!')
            return redirect('recipes:recipe_detail', recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    reviews = recipe.reviews.all()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                recipe=recipe,
                author=form.cleaned_data['author'],
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment']
            )
            messages.success(request, 'Отзыв добавлен!')
            return redirect('recipes:recipe_detail', recipe.id)
    else:
        form = ReviewForm()
    
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'reviews': reviews,
        'form': form,
    })

def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    messages.success(request, f'Рецепт "{recipe.title}" удален')
    return redirect('recipes:index')

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    recipe_id = review.recipe.id
    review.delete()
    messages.success(request, 'Отзыв удален')
    return redirect('recipes:recipe_detail', recipe_id)