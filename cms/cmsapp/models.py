from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class NewUser(AbstractUser):
    profile = models.CharField('profile', default='', max_length=256)

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('column', max_length=256)
    intro = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'column'
        verbose_name_plural = 'column'
        ordering = ['name']


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=128)
    profile = models.CharField('profile', default='', max_length=256)
    password = models.CharField('password', max_length=256)
    register_date = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name


class ArticleManager(models.Manager):
    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query


@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=256)
    column = models.ForeignKey(Column, blank=True, null=True, verbose_name='belong to', on_delete=True)
    author = models.ForeignKey('Author', on_delete=True)
    user = models.ManyToManyField('NewUser', blank=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    published = models.BooleanField('notDraft', default=True)
    poll_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    keep_num = models.IntegerField(default=0)
    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'article'


@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey('NewUser', null=True, on_delete=True)
    article = models.ForeignKey(Article, null=True, on_delete=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    poll_num = models.IntegerField(default=0)

    def __str__(self):
        return self.content


@python_2_unicode_compatible
class Poll(models.Model):
    user = models.ForeignKey('NewUser', null=True, on_delete=True)
    article = models.ForeignKey(Article, null=True, on_delete=True)
    comment = models.ForeignKey(Comment, null=True, on_delete=True)
