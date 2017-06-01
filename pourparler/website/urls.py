import django.views.defaults
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

import website.views

urlpatterns = [
    url(r'^$', website.views.index, name="index"),

    url(r'^new$', website.views.create_event, name="create"),
    url(r'^e/(?P<eid>[-A-Za-z0-9_]+)$', website.views.event, name="event"),
    url(r'^draw/(?P<eid>[-A-Za-z0-9_]+)$', website.views.draw, name="draw"),
    url(r'^submit_subject$', website.views.submit_subject, name="submit_subject"),
    url(r'^submit_subject$', website.views.submit_subject, name="submit_subject"),
    url(r'^speech/(?P<sid>[-A-Za-z0-9_]+)$', website.views.speech, name="speech"),
    url(r'^ds/(?P<sid>[-A-Za-z0-9_]+)$', website.views.del_speech, name="delete-speech"),
    url(r'^register$', website.views.register, name="register"),
    url(r'^login$', website.views.p_login, name="login"),
    url(r'^logout$', website.views.p_logout, name="logout"),
    url(r'^changepwd$', website.views.p_change_pwd, name="change_pwd"),

    url(r'^loc/(?P<uid>[-A-Za-z0-9_]+)$', website.views.profile, name="profile"),
    url(r'^settings$', website.views.user_settings, name="settings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
