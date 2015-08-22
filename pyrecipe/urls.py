from django.conf.urls import include, url
from django.contrib import admin
from recipe.views import RecipeList, RecipeDetail

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RecipeList.as_view(), name='home'),
    url(r'^recipe/(?P<slug>[-\w]+)/$', RecipeDetail.as_view(), name='recipe-detail'),
]
