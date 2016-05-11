from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from gamerauntsia.app.authentication.viewsets import UsersViewSet
router = DefaultRouter()

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

from gamerauntsia.base.feed import LatestEntriesFeed, LatestNewsFeed

admin.autodiscover()

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = patterns('',
     (r'^robots.txt$',
         lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
     (r'^3dedcce0621f78db1fdf62d2bb02148e.txt$',
      lambda r: HttpResponse("3dedcce0621f78db1fdf62d2bb02148e", content_type="text/plain")),

     url(r'^$', 'gamerauntsia.views.index', name='index'),

     # GETB
     url(r'^getb/', include('gamerauntsia.getb.urls')),

     # GAMEPLAYAK
     url(r'^gameplayak/', include('gamerauntsia.gameplaya.urls')),

     # BERRIAK
     url(r'^berriak/(?P<slug>[-\w]+)/$',
         lambda x, slug: HttpResponseRedirect(reverse('berria', args=[slug]))),
     url(r'^bloga/', include('gamerauntsia.berriak.urls'), name='bloga'),

     # DENBORA LERROA
     url(r'^denboralerroa/', include('gamerauntsia.log.urls'), name='log'),

     # JOKOAK
     url(r'^jokoak/', include('gamerauntsia.jokoa.urls'), name='jokoak'),

     # JOKALARIAK
     (r'^komunitatea/', include('gamerauntsia.gamer.urls')),
     (r'^komunitatea/', include('cssocialuser.urls')),
     (r'^komunitatea/', include('registration.backends.default.urls')),

     # AURKEZPENAK
     (r'^aurkezpenak/', include('gamerauntsia.aurkezpenak.urls')),

     # TXAPELKETAK
     (r'^txapelketak/', include('gamerauntsia.txapelketak.urls')),

     # MINECRAFT SERVER
     (r'^zerbitzariak/', include('gamerauntsia.zerbitzariak.urls')),

     # AGENDA
     (r'^agenda/', include('gamerauntsia.agenda.urls')),

     # FOROA
     url(r'^foroa/reset-topics$', 'gamerauntsia.gamer.views.reset_topics', name='reset_topics'),
     url(r'^foroa/', include('django_simple_forum.urls')),

     # KONTAKTUA
     url(r'^kontaktua/$', 'gamerauntsia.kontaktua.views.index', name='kontaktua'),
     url(r'^kontaktua/bidali/$', 'gamerauntsia.kontaktua.views.bidali', name='kontaktua_bidali'),

     # TERMINOLOGIA
     url(r'^terminologia/$', 'gamerauntsia.base.views.index', name='terminologia'),
     url(r'^terminologia/bilatu', 'gamerauntsia.base.views.search_term', name='search_term'),

     # RETRO
     url(r'^jokoen-itzulpenak/$', 'gamerauntsia.retro.views.index', name='retro'),
     url(r'^jokoen-itzulpenak/bilatu', 'gamerauntsia.retro.views.search_retro', name='search_retro'),

     # BILAKETA
     url(r'^bilaketa?(?P<bilatu>[-\w]+)/$', 'gamerauntsia.views.bilaketa', name='bilaketa'),

     # RSS FEED
     url(r'^rss/gameplayak$', LatestEntriesFeed()),
     url(r'^rss/bloga$', LatestNewsFeed()),

     # FB
     url(r'^2b27b83ad50e677714b2dd832b42acc3', include('facebookpagewriter.urls')),

     # COMMENTS
     (r'^comments/', include('django_comments.urls')),

     # KUDEATU
     url(r'^kudeatu/', include(admin.site.urls)),
     url(r'^photologue/', include('photologue.urls', namespace='photologue')),

     # MEZUAK
     (r'^mezuak/', include('django_messages.urls')),

     # EGUTEGIA
     (r'^calendar/', include('django_bootstrap_calendar.urls')),

     # TINYMCE
     (r'^tinymce/', include('tinymce.urls')),

     # APIA
     url(r'^api/1.0/', include('gamerauntsia.api.urls')),

     # APP
     url(r'^app/v1/', include('gamerauntsia.app.authentication.urls')),

     # ERABILERA ETA PRIBATUTASUNA
     (r'^erabilera-baldintzak/$', TemplateView.as_view(template_name='erabilera_baldintzak.html')),
     (r'^pribatutasun-politika/$', TemplateView.as_view(template_name='pribatutasun_politika.html')),
     (r'^gameplay-arauak/$', TemplateView.as_view(template_name='upload_gp.html')),
     (r'^cookie/$', TemplateView.as_view(template_name='cookie.html')),

     # SITEMAP
     url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

     # AJAX ESKAERAK
     url(r'^ajax/get_jokoak/', 'gamerauntsia.gamer.views.get_jokoak', name='ajax_jokoak'),
     url(r'^ajax/get_erabiltzaileak/', 'gamerauntsia.gamer.views.get_user', name='ajax_user'),
     url(r'^ajax/post_finished/', 'gamerauntsia.finished.views.add_finished', name='ajax_finished'),

     url('', include('social.apps.django_app.urls', namespace='social'))

)

router.register(r'profile', UsersViewSet)

if getattr(settings, 'DEBUG', False):
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': getattr(settings, 'STATIC_DOC_ROOT', '')}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': getattr(settings, 'MEDIA_DOC_ROOT', '')}),
    )
