from django.contrib import admin
from recipe.models import Comment, Recipe


class CommentInline(admin.StackedInline):
    model = Comment


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = [
        (None, {
            'fields':   ('name',
                        'slug'
                         )}),
        ('Recipe Description', {
            'fields':   ('description',
                        'created_by',
                        readonly_fields
                       )}),
    ]
    inlines = [CommentInline]

admin.site.register(Recipe, RecipeAdmin)
