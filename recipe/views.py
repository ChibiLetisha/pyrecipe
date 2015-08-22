from django.shortcuts import render
from django.views.generic import ListView
from recipe.models import Recipe


class RecipeList(ListView):
    """
    Lists out the existing recipes.
    """
    model = Recipe
    template_name = 'home.html'
