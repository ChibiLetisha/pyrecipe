from django.shortcuts import render
from django.views.generic import ListView, DetailView
from recipe.models import Recipe


class RecipeList(ListView):
    """
    Lists out the existing recipes.
    """
    model = Recipe
    template_name = 'home.html'


class RecipeDetail(DetailView):
    """
    Shows the details of the chosen recipe.
    Name/Description/Who wrote it(created_by)/
    When it was written(created)/Comments
    """
    model = Recipe
    template_name = 'recipe.html'
