from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    name =  models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    class Meta:
        ordering = ['-name']

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe)
    comment_text = models.TextField()
    commenter = models.ForeignKey(User)
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-commented_at']

    def __unicode__(self):
        return 'Created by: ' + self.commenter.username + ' at ' + self.commented_at.strftime('%Y-%m-%d %H:%M')
