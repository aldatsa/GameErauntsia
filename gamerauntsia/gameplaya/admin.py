from gamerauntsia.gameplaya.models import GamePlaya, Kategoria, Zailtasuna, BideoPlataforma
from django.contrib import admin
from django.conf import settings
from gamerauntsia.gameplaya.forms import GamePlayAdminForm
from django.utils.safestring import mark_safe


class GamePlayAdmin(admin.ModelAdmin):

    @mark_safe
    def admin_thumbnail(self,obj):
        try:
            if obj.argazkia:
                return u'<img src="%s" />' % (obj.argazkia.get_admin_thumbnail_url())
            else:
                return u'(Irudirik ez)'
        except:
            return '%s' % (obj.argazkia.title)
    admin_thumbnail.short_description = 'Thumb'

    @mark_safe
    def preview(self,obj):
        return '<a href="/gameplayak/%s">aurreikusi</a>' % (obj.slug)

    list_display = ['admin_thumbnail','izenburua', 'preview','zailtasuna', 'jokoa','plataforma','pub_date', 'erabiltzailea','publikoa_da', 'status','shared']
    list_display_links = ['izenburua', ]
    prepopulated_fields = {"slug": ("izenburua",)}
    filter_horizontal = ['kategoria', ]
    raw_id_fields = ['argazkia','jokoa','plataforma','erabiltzailea']
    list_filter = ['zailtasuna', 'publikoa_da', 'status']
    search_fields = ['erabiltzailea__fullname','erabiltzailea__username','izenburua']
    ordering = ['-pub_date', ]
    form = GamePlayAdminForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or (obj and request.user != obj.erabiltzailea and request.user.belongs_group(settings.GP_GROUP)):
            return super(GamePlayAdmin, self).get_readonly_fields(request, obj)
        else:
            return ('status',)

    def queryset(self, request):
        qs = super(GamePlayAdmin, self).queryset(request)
        if request.user.is_superuser or request.user.belongs_group(settings.GP_GROUP):
            return qs
        else:
            return qs.filter(erabiltzailea = request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or obj.erabiltzailea == request.user or request.user.belongs_group(settings.GP_GROUP):
            return True
        else:
            return False

    has_delete_permission = has_change_permission

class KategoriaAdmin(admin.ModelAdmin):
    list_display = ['izena','slug']
    prepopulated_fields = {"slug": ("izena",)}

class ZailtasunAdmin(admin.ModelAdmin):
    list_display = ['izena', ]
    prepopulated_fields = {"slug": ("izena",)}

class BideoPlataformaAdmin(admin.ModelAdmin):
    list_display = ['izena', ]

admin.site.register(GamePlaya, GamePlayAdmin)
admin.site.register(Kategoria, KategoriaAdmin)
admin.site.register(Zailtasuna, ZailtasunAdmin)
admin.site.register(BideoPlataforma, BideoPlataformaAdmin)
