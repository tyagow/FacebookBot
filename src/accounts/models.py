from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify


def create_slug(instance, new_slug=None):
    slug = slugify(instance.user.username)
    if new_slug is not None:
        slug = new_slug
    qs = Profile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


class Profile(models.Model):
    fbid = models.CharField(blank=True, max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(null=True, unique=True)
    picture = models.URLField(blank=True)
    first_name = models.CharField(blank=True, max_length=40)
    last_name = models.CharField(blank=True, max_length=40)
    timezone = models.IntegerField(blank=True, null=True)
    gender = models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)
    telefone = models.CharField(blank=True, max_length=20)
    endereco = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.user.username

    def save_details(self, fbid, user_details):
        self.fbid = fbid
        self.picture = user_details.get('profile_pic')
        self.first_name = user_details.get('first_name')
        self.last_name = user_details.get('last_name')
        gender = user_details.get('gender')
        if gender == 'male':
            self.gender = 'M'
        else:
            self.gender = 'F'
        self.timezone = user_details.get('timezone')
        self.save()

    def update_or_create_session(self):
        """
        Must update last valid session or create a new one
        :return:  :bool: created, :Session: session
        """
        # get last active session
        created = False
        session = self.sessions.active()

        # Create session
        if not session:
            created = True
            session = self.sessions.create()
        else:
            # verify if session is valid ( expired ...)
            if session.is_valid():
                # Force update model to updated last_active
                session.save()
            else:
                # create new session
                created = True
                session = self.sessions.create()
        return created, session

    @property
    def session(self):
        return self.sessions.active()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_save, sender=Profile)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
