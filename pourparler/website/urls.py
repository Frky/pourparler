import django.views.defaults
from django.conf.urls import url

import website.views

urlpatterns = [
    url(r'^$', website.views.index, name="index"),

    url(r'^new$', website.views.create_event, name="create"),
    url(r'^e/(?P<eid>[-A-Za-z0-9_]+)$', website.views.event, name="event"),

    url(r'^register$', website.views.register, name="register"),
    url(r'^login$', website.views.p_login, name="login"),
    url(r'^logout$', website.views.p_logout, name="logout"),
]
