from django import forms
from django.utils.safestring import mark_safe
from gamerauntsia.berriak.models import Berria, Gaia
from gamerauntsia.gamer.models import GamerUser, JokuPlataforma, AmaitutakoJokoak
from gamerauntsia.gameplaya.models import Kategoria, GamePlaya, BideoPlataforma
from gamerauntsia.jokoa.models import Jokoa
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext as _
from django.conf import settings
from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import ReCaptchaField
import re

TINYMCE_SMALL_BODY_CONFIG = getattr(settings, 'TINYMCE_SMALL_BODY_CONFIG', {})
TINYMCE_DEFAULT_CONFIG = getattr(settings, 'TINYMCE_DEFAULT_CONFIG', {})


class ProfileForm(forms.ModelForm):

    class Meta:
        model = GamerUser
        fields = ('fullname','bio',)


class ProfilePhotoForm(forms.Form):
    avatarpic  = forms.ImageField(label=_('Your picture'),help_text=_('Please upload a picture of you. Supported formats: jpg, png, gif.'))

    def clean_argazkia(self):
        """ """
        avatarpic = self.cleaned_data['avatarpic']
        name = avatarpic.name
        try:
            name.encode('ascii')
        except:
            raise forms.ValidationError(_('The name of the picture (%s) has an unsupported character. Please rename it before uploading.') % name)

        format = name.split('.')[-1]
        if format.lower().strip()==u'bmp':
            raise forms.ValidationError(_("The picture is not in one of our supported formats. We don't support BMP files. Please change it"))


class GamerForm(forms.ModelForm):

    signature = forms.CharField(widget=TinyMCE(
           attrs={'cols': 80, 'rows': 15,},mce_attrs=TINYMCE_SMALL_BODY_CONFIG),required=False)

    class Meta:
        model = GamerUser
        fields = ('fullname','bio','twitter_id', 'mastodon_id','facebook_id','telegram_id','signature')

class ChannelsForm(forms.ModelForm):
    class Meta:
        model = GamerUser
        widgets = {'channel_description': forms.Textarea(),
                   'twitch_channel': forms.TextInput(attrs={'placeholder':'Erabiltzaile izena, ez URLa'}),
                   'ytube_channel': forms.URLInput(attrs={'placeholder': 'URLa'}),
                   'peertube_channel': forms.URLInput(attrs={'placeholder': 'URLa'})}
        fields = ('channel_description','ytube_channel','twitch_channel', 'peertube_channel')

class PCForm(forms.ModelForm):
    class Meta:
        model = GamerUser
        fields = ('motherboard','processor','graphics','soundcard','ram','harddrive','harddrive2','mouse','keyboard','speakers')

class NotifyForm(forms.ModelForm):

    class Meta:
        model = GamerUser
        fields = ('email_notification','buletin_notification')

class ArticleForm(forms.ModelForm):

    desk = forms.CharField(label='',widget=TinyMCE(
           attrs={'cols': 80, 'rows': 15,},mce_attrs=TINYMCE_DEFAULT_CONFIG))

    gaia = forms.ModelMultipleChoiceField(label='Gaiak', queryset=Gaia.objects.all(),
        widget=forms.SelectMultiple(attrs={'size':'15'}),help_text='Aukeratu artikuluarekin zer ikusia duen gai bat edo gehiago')

    argazkia  = forms.ImageField(label='Nabarmendutako irudia', help_text='Onartutako formatuak: jpg, png, gif.', required=False)

    def clean_desk(self):
        """ """
        desk = self.cleaned_data['desk'].strip()
        if not desk:
            raise forms.ValidationError('Mezu hutsek ez dute balio. Mesedez, idatzi zerbait!')
        return self.cleaned_data['desk']

    class Meta:
        model = Berria
        exclude = ('slug','erabiltzailea','pub_date','publikoa_da','status','mod_date','shared')

class GameCatalogForm(forms.ModelForm):
    bertsioa = forms.CharField(label='Bertsioa (aukerazkoa)', help_text="Joko saga bat bada, zehaztu hemen bertsioa. ", required=False)
    logoa  = forms.ImageField(label='Jokoaren logo ofiziala', help_text='Onartutako formatuak: jpg, png, gif.', required=False)
    desk = forms.CharField(label="Deskribapen laburra (aukerazkoa)", widget=forms.Textarea,required=False)
    trailer = forms.CharField(label='Youtube trailerra (aukerazkoa)', help_text="Steam ID zenbakia jarrita badago, ez da beharrezkoa. Bestela, Youtube bideoaren KODEA itsatsi. Adibidez: bkgzXpKbVGE", required=False)
    wiki = forms.CharField(label='Wikia (aukerazkoa)', help_text="Eremu honetan joko honen wikipediako URL helbidea zehaztu mesedez.", required=False)
    steam_id = forms.IntegerField(label="Steam ID (aukerazkoa)", help_text="Jokoa Steam plataforman aurki badaiteke, jokoaren fitxaren URLan agertzen den zenbakia. Adibidez: 236110",required=False)

    class Meta:
        model = Jokoa
        fields = ('izena','bertsioa','desk','logoa','lizentzia','url','steam_id','trailer','wiki')

class TopForm(forms.ModelForm):

    top_jokoak = forms.ModelMultipleChoiceField(queryset=Jokoa.objects.all().order_by('izena','bertsioa'),
                                          label='',
                                          required=False,
                                          widget=forms.MultipleHiddenInput())

    class Meta:
        model = GamerUser
        fields = ('top_jokoak',)

class GameForm(forms.ModelForm):

    class Meta:
        model = JokuPlataforma
        fields = ('plataforma','nick')

class AmaitutaForm(forms.ModelForm):

    class Meta:
        model = AmaitutakoJokoak
        fields = ('izenburua','urtea')



class GamePlayForm(forms.ModelForm):

    desk = forms.CharField(label='',widget=TinyMCE(
           attrs={'cols': 80, 'rows': 15,},mce_attrs=TINYMCE_SMALL_BODY_CONFIG))

    kategoria = forms.ModelMultipleChoiceField(label='Gaiak', queryset=Kategoria.objects.all(),
        widget=forms.SelectMultiple(attrs={'size':'15'}),help_text='Aukeratu artikuluarekin zer ikusia duen gai bat edo gehiago')

    argazkia  = forms.ImageField(label='Nabarmendutako irudia', help_text='Onartutako formatuak: jpg, png, gif.', required=False)

    jokoa = forms.ModelChoiceField(label="Jokoa", queryset=Jokoa.objects.all().order_by('izena'))

    bideo_plataforma = forms.ModelChoiceField(label="Bideo plataforma",
                                              help_text='Zure plataforma falta bada jarri gurekin harremanetan, eta gehituko dugu zerrendara',
                                              initial=1,
                                              queryset=BideoPlataforma.objects.all().order_by('izena'))

    lizentzia = forms.BooleanField(label="Irakurri eta onartzen ditut gameplayak igotzeko arauak", help_text=mark_safe('Informazioa gehiago <a href="/gameplay-arauak">gameplay arauetan</a>.'))

    def clean_lizentzia(self):
        lizentzia = self.cleaned_data['lizentzia']
        if not lizentzia:
            raise forms.ValidationError('Gameplaya igotzeko arauak onartzea beharrezkoa da. Mesedez, irakurri eta onartu arauak.')
        return self.cleaned_data['lizentzia']

    def clean_iraupena_min(self):
        minutu = self.cleaned_data['iraupena_min']
        if minutu == 0:
            raise forms.ValidationError('Bideoaren iraupena zehaztea garrantzitsua da. Mesedez, sartu denbora!')
        return self.cleaned_data['iraupena_min']

    def clean_desk(self):
        """ """
        desk = self.cleaned_data['desk'].strip()
        if not desk:
            raise forms.ValidationError('Mezu hutsek ez dute balio. Mesedez, idatzi zerbait!')
        return self.cleaned_data['desk']

    def clean_bideoa(self):
        bideoa = self.cleaned_data['bideoa']
        if not bideoa:
            raise forms.ValidationError('Bideoaren kodea derrigorrezkoa da!')
        elif not re.fullmatch(r"^[a-zA-Z\-0-9]+$", bideoa):
            raise forms.ValidationError('Bideoaren kodea bakarrik jarri behar da. Mesedez, ikusi adibidea eta zuzendu kodea!')
        return bideoa

    class Meta:
        model = GamePlaya
        fields = ('izenburua', 'desk', 'bideo_plataforma', 'bideoa',
                  'iraupena_min', 'iraupena_seg', 'jokoa','plataforma',
                  'zailtasuna','kategoria', 'argazkia', 'lizentzia')
        exclude = ('slug','erabiltzailea','pub_date','publikoa_da','status','mod_date','shared','argazkia')

class RecaptchaRegistrationForm(RegistrationFormUniqueEmail):
    recaptcha = ReCaptchaField(label="")
