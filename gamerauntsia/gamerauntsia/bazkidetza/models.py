from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from gamerauntsia.gamer.models import GamerUser
from gamerauntsia.jokoa.models import Jokoa, Plataforma
from photologue.models import Photo
from datetime import datetime
from django.utils import timezone
import telebot

ESKAINTZA_MOTAK = (
    (1, 'Eskatzekoa'),
    (2, 'Parte hartzekoa'),
    (3, 'Eskubidea'),
)

DENDA_CHOICES = (
    (1, 'Steam'),
    (2, 'Origin'),
)

class Bazkidea(models.Model):
    user = models.ForeignKey(GamerUser, unique=True)
    paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    expire_date = models.DateTimeField(default=timezone.localtime(timezone.now().replace(year=timezone.now().year + 1)))

    def has_eskaera(self):
        return Eskaera.objects.filter(bazkidea=self, is_active=True).exists()

    def has_partaidetza_eskaera(self):
        return Eskaera.objects.filter(bazkidea=self, mota=2, is_active=True).exists()

    def get_eskaerak(self):
        eskaerak = Eskaera.objects.filter(bazkidea=self, is_active=True).order_by("-added")
        return eskaerak

    class Meta:
        verbose_name = "Bazkidea"
        verbose_name_plural = "Bazkideak"

    def __unicode__(self):
        return u'#%d %s' % (self.id, self.user.username)


class Eskaintza(models.Model):
    izena = models.CharField(max_length=150)
    slug = models.SlugField()
    deskribapena = models.TextField()
    irudia = models.ForeignKey(Photo)

    mota = models.IntegerField(choices=ESKAINTZA_MOTAK, default=1)

    activate_date = models.DateTimeField(auto_now_add=True, editable=False)
    expire_date = models.DateTimeField(null=True, blank=True)

    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Eskaintza"
        verbose_name_plural = "Eskaintza"

    def __unicode__(self):
        return u'%s' % (self.izena)

    def get_absolute_url(self):
        return reverse('eskaintza', arg=[self.slug])


class Eskaera(models.Model):
    eskaintza = models.ForeignKey(Eskaintza)
    bazkidea = models.ForeignKey(Bazkidea)

    added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Eskaera"
        verbose_name_plural = "Eskaerak"

    def __unicode__(self):
        return u'%s (#%d %s)' % (self.eskaintza.izena, self.bazkidea.id, self.bazkidea.user.username)


class OparitzekoJokoak(models.Model):
    key = models.CharField(max_length=250)
    non_aldatzeko = models.IntegerField(choices=DENDA_CHOICES, default=1)
    jokoa = models.ForeignKey(Jokoa)
    plataforma = models.ForeignKey(Plataforma)

    oparituta = models.BooleanField(default=False)

    pub_date = models.DateTimeField('publikazio data', default=datetime.now)

    class Meta:
        verbose_name = "Oparitzeko jokoa"
        verbose_name_plural = "Oparitzeko jokoak"

    def __unicode__(self):
        return u'%s' % (self.jokoa.izena)


def send_member_msg(sender,instance,**kwargs):
    if kwargs['created']:
        tb = telebot.TeleBot(settings.TELEBOT_TOKEN)
        message = '[#%s Bazkidea]\n%skudeatu/bazkidetza/bazkidea/%s' % (instance.id, settings.HOST, instance.id)
        tb.send_message(settings.ADMIN_CHAT_ID, message)

post_save.connect(send_member_msg, sender=Bazkidea)
