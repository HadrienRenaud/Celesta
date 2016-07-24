from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accueil', views.accueil),
    url(r'^connexion$', views.connexion, name='connexion'),
    url(r'^(?P<folder>.*)deconnexion/?$', views.deconnexion, name='deconnexion'),
    url(r'^(?P<folder>.*)index', views.index, name='index'),
    url(r'^(?P<folder>.*)/?', views.index, name='index')
]
