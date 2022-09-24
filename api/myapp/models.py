from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
MAX_LENGTH = 100


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    username = models.CharField(_('Username'), unique=True, max_length=MAX_LENGTH)
    bio = models.TextField(_('Biography'), blank=True)
    image = models.ImageField(_('Image'), null=True)
    date_of_joining = models.DateTimeField(_('Date joined'), auto_now_add=True)
    data_of_birth = models.DateField(_('Date of birth'), blank=True, null=True )
    subscriptions = models.ManyToManyField('self',  symmetrical=False,
                                           verbose_name=_('Subscriptions'),
                                           blank=True,
                                           related_name='subscription')
    subscribers = models.ManyToManyField('self',  symmetrical=False,
                                         verbose_name=_('Subscribers'),blank=True, related_name='subscriber')
    # favourites = models.ManyToManyField('Article', verbose_name=_('Favorite articles'), related_name=)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# class Article(models.Model):
#     title = models.CharField(_('Title'), max_length=MAX_LENGTH)
#     description = models.TextField(_('Description'))
#     body = models.TextField(_('Text'))
#     created = models.DateTimeField(_('Creation date'), auto_now_add=True)
#     updated = models.DateTimeField(_('Update date'), auto_now=True)
#     author = models.ForeignKey(CustomUser, _('Author'), models.CASCADE)
#     slug = models.SlugField(CustomUser, _('Slug'), models.CASCADE)
#
#
# class Comments(models.Model):
#     author = models.ForeignKey(CustomUser, _('Author'), models.CASCADE)
#     body = models.TextField(_('Body'))
#     likes = models.Count(_('Number of likes'))
#     dislikes = models.Count(_('Number of dislikes'))
#     reply = models.ForeignKey('self', , models.CASCADE)