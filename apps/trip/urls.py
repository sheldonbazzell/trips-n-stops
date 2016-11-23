"""triptracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r"^data/(?P<location>(\S+\s*){1,})/(?P<term>[a-zA-Z0-9]*?)$", views.yelp),
    url(r'^process_save$',views.process_save),
    url(r'^show_route/(?P<trip_id>\d+?)$',views.show_route),
    url(r'^login$',views.login_check),
    url(r'^register$',views.register),
    url(r'^logout$',views.logout),
    url(r"^add_comment/(?P<trip_id>\d+?)",views.add_comment),
]
