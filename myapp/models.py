from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from taggit.managers import TaggableManager

MAX_LENGTH = 100


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    username = models.CharField(_('Username'), unique=True, max_length=MAX_LENGTH)
    name = models.CharField(_('Name'), max_length=MAX_LENGTH, blank=True)
    surname = models.CharField(_('Surname'), max_length=MAX_LENGTH, blank=True)
    bio = models.TextField(_('Biography'), blank=True)
    image = models.ImageField(_('Image'), null=True, blank=True)
    date_of_joining = models.DateTimeField(_('Date joined'), auto_now_add=True)
    date_of_birth = models.DateField(_('Date of birth'), blank=True, null=True)
    sent_requests = models.ManyToManyField('self', related_name='followers', symmetrical=False,
                                           verbose_name=_('Sent followers'), blank=True)
    favorites = models.ManyToManyField('Article', related_name='users_favorites',
                                        verbose_name=_('Favorites articles'), blank=True)
    liked_articles = models.ManyToManyField('Article', related_name='users_liked_article', blank=True)
    disliked_articles = models.ManyToManyField('Article', related_name='users_disliked_article', blank=True)
    liked_comments = models.ManyToManyField('Comment', related_name='users_liked_comment', blank=True)
    disliked_comments = models.ManyToManyField('Comment', related_name='users_disliked_comment', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.username} - {self.name} - {self.surname}"


class CustomModel(models.Model):
    """All inherited models from CustomModel will have created and updated"""

    createdAt = models.DateTimeField(_('Creation date'),  auto_now_add=True, editable=True,)
    updatedAt = models.DateTimeField(_('Update date'), auto_now=True, editable=True,)

    class Meta:
        abstract = True


class Article(CustomModel):
    title = models.CharField(_('Title'), max_length=MAX_LENGTH)
    description = models.TextField(_('Description'))
    body = models.TextField(_('Text'))
    author = models.ForeignKey(CustomUser, models.CASCADE, related_name='articles',
                               verbose_name=_('Author'))
    slug = models.SlugField(_('Slug'), unique=True)
    tagList = TaggableManager(blank=True)

    def likesCount(self):
        return self.users_liked_article.count()

    def dislikesCount(self):
        return self.users_disliked_article.count()

    def favorites(self):
        return self.users_favorites.all()

    def favoritesCount(self):
        return self.favorites().count()


class Comment(CustomModel):

    author = models.ForeignKey(CustomUser, models.SET_NULL, related_name='comments',
                                verbose_name=_('Author'), null=True)
    article = models.ForeignKey(Article, models.CASCADE, related_name='comments',
                                verbose_name=_('Article'))
    body = models.TextField(_('Body'))
    changed = models.BooleanField(default=False, blank=True)
    parent = models.ForeignKey('self', models.CASCADE, related_name='child',
                                verbose_name=_('Parent'), blank=True, null=True)

    def likesCount(self):
        return self.users_liked_comment.count()

    def dislikesCount(self):
        return self.users_disliked_comment.count()
