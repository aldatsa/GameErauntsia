from django import template
from django.utils.safestring import mark_safe
from gamerauntsia.gameplaya.models import GamePlaya
from gamerauntsia.berriak.models import Berria
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('top_gameplayak.html')
def top_gameplayak():
    h = {}
    h['zerr_tutoriala'] = GamePlaya.objects.filter(publikoa_da=True).order_by('-pub_date')[:10]
    return h
 
@register.inclusion_tag('behe_blokeak.html') 
def azken_berriak():
    h = {}
    h['berriak'] = Berria.objects.all().order_by('-pub_date')[:5]
    return h

@register.filter
def mainmenu(url):
    """ """
    mainmenulist = (('','Sarrera'),('gameplayak','GamePlayak'),('jokoak','Jokoak'),('gaiak','Gaiak'),('berriak','Berriak'),('nor-gara','Nor gara'),('kontaktua','Kontaktua'))
    mainmenu = []
    links = url.strip('/').split('/')
    selected_mainmenu=''
    if len(links)>0 and not links[0]=='':
        selected_mainmenu=links[0]
    for link,title in mainmenulist:
        if selected_mainmenu==link and len(links)>1:
            mainmenu.append('<li class="active"><a href="/%s" title="%s">%s</a></li>' % (link,title,title))      
        elif selected_mainmenu==link:
            mainmenu.append('<li class="active">%s</li>' % (title))
        else:
            if link=='' and selected_mainmenu=='sarrera':
                mainmenu.append('<li class="active"><a href="/" title="%s">%s</a></li>' % (title,title))
            else:
                mainmenu.append('<li><a href="/%s" title="%s">%s</a></li>' % (link,title,title))
    return mark_safe(''.join(mainmenu))

@register.filter
def tabmenu(url):
    """ """
    mainmenulist = (('','Azkenak'),('bozkatuenak','Bozkatuenak'))
    mainmenu = []
    links = url.strip('/').split('/')
    selected_mainmenu=''
    if len(links)>0 and not links[0]=='':
        selected_mainmenu=links[1]
    for link,title in mainmenulist:
        if selected_mainmenu==link:
            mainmenu.append('<li class="selected">%s</li>' % (title))     
        else:
            if selected_mainmenu=='':
                mainmenu.append('<li><a href="/sarrera/%s" title="%s">%s</a></li>' % (link,title,title))
            else:
                mainmenu.append('<li><a href="/%s" title="%s">%s</a></li>' % (link,title,title))
    return mark_safe(''.join(mainmenu))

@register.filter
def get_bideo(item):
    html = ''
    if item.bideoa.startswith('http://vimeo.com'):
        html = '<iframe class="shadow" src="http://player.vimeo.com/video/'+item.get_url()+'" width="500" height="281" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>'
    elif item.bideoa.startswith('http://youtu.be'):
        html = '<iframe class="shadow" width="500" height="281" src="http://www.youtube.com/embed/'+item.get_url()+'" frameborder="0" allowfullscreen></iframe>'
    else:
        html = ''
    return html

@register.filter
def get_fullname(username):
    user = User.objects.get(username=username)
    return '%s %s' % (user.first_name, user.last_name)    