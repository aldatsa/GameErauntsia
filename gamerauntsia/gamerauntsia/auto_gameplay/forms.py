from django import forms
from django.conf import settings
from gamerauntsia.auto_gameplay.models import AutoGamePlaya
from tinymce.widgets import TinyMCE

TINYMCE_DEFAULT_CONFIG = getattr(settings, 'TINYMCE_DEFAULT_CONFIG', {})

class AutoGamePlayAdminForm(forms.ModelForm):
    desk = forms.CharField(widget=TinyMCE(
               attrs={'cols': 80, 'rows': 50,},mce_attrs=TINYMCE_DEFAULT_CONFIG))

    class Meta:
        model = AutoGamePlaya
        fields = '__all__'