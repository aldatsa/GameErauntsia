from gamerauntsia.berriak.models import Berria, Gaia
from django.contrib import admin
from gamerauntsia.berriak.forms import BerriaAdminForm

class BerriakAdmin(admin.ModelAdmin):

    def admin_thumbnail(self,obj):
        if obj.argazkia:
            return u'<img src="%s" />' % (obj.argazkia.get_admin_thumbnail_url())
        else:
            return u'(Irudirik ez)'
    admin_thumbnail.short_description = 'Thumb'
    admin_thumbnail.allow_tags = True

    def preview(self,obj):
        return '<a href="/bloga/%s">%s</a>' % (obj.slug, obj.slug)
    preview.allow_tags=True

    list_display = ('izenburua', 'preview', 'erabiltzailea', 'pub_date', 'mod_date', 'status','admin_thumbnail')
    prepopulated_fields = {"slug": ("izenburua",)}
    filter_horizontal = ('gaia',)
    list_filter = ('erabiltzailea', 'status')
    search_fields = ['erabiltzailea__username','erabiltzailea__fullname','izenburua']
    raw_id_fields = ('argazkia','erabiltzailea')
    ordering = ('-pub_date',)
    form = BerriaAdminForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(BerriakAdmin, self).get_readonly_fields(request, obj)
        else:
            return ('status',)

    def queryset(self, request):
        qs = super(BerriakAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(erabiltzailea = request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.erabiltzailea = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or obj.erabiltzailea == request.user:
            return True
        else:
            return False

    has_delete_permission = has_change_permission


class GaiaAdmin(admin.ModelAdmin):
    list_display = ('izena','slug')
    prepopulated_fields = {"slug": ("izena",)}


admin.site.register(Gaia, GaiaAdmin)
admin.site.register(Berria, BerriakAdmin)
