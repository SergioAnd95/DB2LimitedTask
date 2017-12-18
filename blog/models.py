from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(likes_count=models.Count('likes'))


class Post(models.Model):
    title = models.CharField(_('Title'), max_length=256)
    preview_text = models.TextField(_('Preview text'), blank=True, null=True)
    main_image = models.ImageField(_('Main image'), upload_to='post')
    body = models.TextField(_('Body'))
    author = models.ForeignKey(
        User,
        related_name='posts',
        verbose_name=_('Author')
    )

    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('Date modified'), auto_now=True)

    class Meta:
        ordering = ('date_created', )

    def __str__(self):
        return self.title

    def get_preview_text(self):
        return self.preview_text if self.preview_text else self.body[:300]+'...'

    def user_like_exist(self, user):
        return self.likes.filter(user=user).count() > 0


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        related_name='comments',
        verbose_name=_('Author')
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        verbose_name=_('Post')
    )
    body = models.TextField(_('Body'))

    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)

    def __str__(self):
        return "Comment %s by %s" %(self.post.title, self.author.email)


class Like(models.Model):
    user = models.ForeignKey(
        User,
        related_name='likes',
        verbose_name=_('User')
    )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        verbose_name=_('Post')
    )

    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')