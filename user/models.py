from .managers import UserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name=_('email address'), unique=True, blank=True)
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus last_name, with a space in between
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this User.
        """

    def clean(self):
        super(User, self).clean()
        if not self.username:
            raise ValidationError(_('Provide at least phone or email'))
