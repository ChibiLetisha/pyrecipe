from django.conf.urls import include, url
from django.contrib import admin
from recipe.views import RecipeList

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RecipeList.as_view(), name='home')
]
