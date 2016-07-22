from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^date$', views.date_actuelle),
    url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition),
    url(r'^accueil', views.accueil),
    url(r'^$', views.accueil),
    url(r'^(?P<folder>.*)index', views.index, name='index'),
    url(r'^(?P<folder>.*)/', views.index, name='index')
]
