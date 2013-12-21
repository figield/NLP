from django.conf.urls.defaults import *
from translator import media

urlpatterns = patterns('',
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': media.__path__[0], 'show_indexes': True})
)

urlpatterns += patterns('phrase.views',
           (r'^$', 'main_page'),
           (r'^translate/$', 'translate'),
           (r'^translate_ang/$', 'translate_ang'),
           (r'^translate/go_and_translate/$', 'go_and_translate'),
           (r'^translate/go_and_translate_ang/$', 'go_and_translate_ang'),
           (r'^credits/$', 'credits'),
           (r'^phrase/$', 'phrase'),
           (r'^dictionary/$', 'dictionary'),
           (r'^sentence/$', 'sentence'),
           (r'^find_sentence/$', 'find_sentence'),
           (r'^find_phrase/$', 'find_phrase'),
           (r'^find_word/$', 'find_word')
)
