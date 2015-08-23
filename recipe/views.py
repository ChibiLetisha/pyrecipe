from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms import modelform_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, DetailView, CreateView, View, FormView, RedirectView
from recipe.models import Recipe, Comment


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


class NewComment(LoginRequiredMixin, CreateView):
    """
    Saves comments posted by logged in users.
    """
    model = Comment
    fields = ['comment_text']

    @staticmethod
    def get(request, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        comment = form.save(commit=False)
        recipe = Recipe.objects.get(slug=self.kwargs['slug'])
        comment.commenter = self.request.user
        comment.recipe = recipe
        comment.save()
        return super(NewComment, self).form_valid(form)

    def get_success_url(self):
        return reverse('recipe-detail', kwargs={'slug': self.kwargs['slug']})


class Register(CreateView):
    """
    Registers an user with username and password.
    """
    model = User
    template_name = 'register_form.html'
    success_url = reverse_lazy('login')
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


class Login(FormView):
    """
    Logs in a registered user if the username and the password is valid.
    """
    form_class = AuthenticationForm
    template_name = 'login_form.html'

    def form_valid(self, form):
        redirect_to = reverse_lazy('home')
        login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(redirect_to)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)


class Logout(RedirectView):
    """
    Logs out the current user.
    """
    url = reverse_lazy('home')
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).dispatch(request, *args, **kwargs)
