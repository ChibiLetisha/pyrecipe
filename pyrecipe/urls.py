from django.conf.urls import include, url
from django.contrib import admin
from recipe.views import RecipeList, RecipeDetail, Register, NewRecipe, Login, Logout, NewComment

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RecipeList.as_view(), name='home'),
    url(r'^new-recipe/$', NewRecipe.as_view(), name='new-recipe'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^recipe/new-comment/(?P<slug>[-\w]+)/$', NewComment.as_view(), name='new-comment'),
    url(r'^recipe/(?P<slug>[-\w]+)/$', RecipeDetail.as_view(), name='recipe-detail'),
]
