from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.forms import modelform_factory
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, View
from recipe.models import Recipe


class LoginRequiredMixin(View):
    """
    Checks if user has been logged in.
    Doesn't let unauthorized people access the page.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


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


class NewRecipe(LoginRequiredMixin, CreateView):
    """
    Saves recipe created by logged in user.
    """
    model = Recipe
    template_name = 'register_form.html'
    success_url = reverse_lazy('home')
    fields = ['name', 'description']

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.created_by = self.request.user
        recipe.slug = slugify(recipe.name)
        recipe.save()
        return super(NewRecipe, self).form_valid(form)


class Register(CreateView):
    """
    Registers an user with username and password.
    """
    model = User
    template_name = 'register_form.html'
    success_url = reverse_lazy('home')
    fields = ['username', 'password']
    widgets = {
        'password': forms.PasswordInput
    }

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        return super(Register, self).form_valid(form)

    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)

