from gamerauntsia.berriak.models import Berria
from django.contrib import admin
from gamerauntsia.berriak.forms import BerriaAdminForm

class BarriakAdmin(admin.ModelAdmin):
    list_display = ('izenburua', 'slug', 'erabiltzailea', 'pub_date', 'mod_date', 'publikoa_da')
    prepopulated_fields = {"slug": ("izenburua",)}
    form = BerriaAdminForm	
	
admin.site.register(Berria, BarriakAdmin)
