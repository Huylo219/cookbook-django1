from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
]