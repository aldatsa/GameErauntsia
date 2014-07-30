from django.db import models
from photologue.models import Photo

SOFTWARE_AUKERAK = (
        ('C', 'Copyright'),
        ('FR', 'Doakoa'),
        ('OS', 'Kode Irekia'),
    )	

class Jokoa(models.Model):
    izena = models.CharField(max_length=64)
    slug = models.SlugField(db_index=True, help_text="Eremu honetan joko honen URL helbidea zehazten ari zara.")
    desk = models.TextField(max_length=256,null=True,blank=True)
    bertsioa = models.CharField(max_length=64,null=True,blank=True)
    lizentzia = models.CharField(max_length=2, null=True,blank=True, choices=SOFTWARE_AUKERAK)
    
    logoa = models.ForeignKey(Photo,null=True,blank=True)
    url = models.CharField(max_length=64, help_text="Eremu honetan joko honen atariko URL helbidea zehazten ari zara." )
    wiki = models.CharField(max_length=64, null=True, blank=True, help_text="Eremu honetan joko honen wikipediako URL helbidea zehaztu mesedez." )
    
    
    class Meta:
        verbose_name = "jokoa"
        verbose_name_plural = "jokoak"
        
    def __unicode__(self):
        return u'%s %s' % (self.izena, self.bertsioa)
