# *****************************  Imports  ******************************


# django
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.http.response import HttpResponseRedirect
# modules perso
from .forms import ConnexionForm
from . import models

# autres modules
from pathlib import Path
from re import search


# ***********************  Traitement de données  ************************


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def actionneur(extension):
    return []


class Dossier:

    def __init__(self, folder=''):
        self.folder = folder
        self.path_obj = Path(folder)
        self.iterdir = self.path_obj.iterdir

    def getFiles(self, folder=''):
        return [file for file in self.iterdir()]

    def getBlocs(self):
        blocList = []
        for file in self.getFiles():
            nomFichier = str(file).split('/')[-1]
            title = nomFichier
            if '.' in nomFichier:
                extension = title.split('.')[-1]
            else:
                extension = ""
            commentaire = "File : " + \
                str(file) + " Extension : " + extension
            actions = actionneur(extension)
            blocList.append(
                Bloc(title=title, commentaire=commentaire, actions=actions))
        return blocList


class Bloc:

    def __init__(self, title='', commentaire='', actions=[]):
        self.title = title
        self.commentaire = commentaire
        self.actions = actions
        self.hasCommentaire = (len(commentaire) > 0)
        self.hasActions = (len(actions) > 0)


class Action:

    def __init__(self, title="", onclic=""):
        self.title = title
        self.onclic = onclic


class SubtitleLink:

    def __init__(self, text="", link=""):
        self.text = text
        self.link = link


def subtitleur(folder):
    foldList = folder.split('/')
    subtitleList = []
    for i, sub in enumerate(foldList):
        subtitleList.append(SubtitleLink(
            text=sub, link='/'.join(foldList[:i + 1])))
    subtitleList.reverse()
    return subtitleList


def carteur(folder):
    if folder == 'None' or folder == "" or folder == "deconnexion":
        return {'folder': "None", 'subtitle': [SubtitleLink(text='Index')], 'cartes': []}
    try:
        cartes = Dossier("bouzzi/links/" + folder).getBlocs()
    except FileNotFoundError:
        raise Http404(
            "FileNotFoundError : Ceci n'est pas un dossier valide : " + folder)
    context = {
        'folder': folder,
        'subtitle': subtitleur(folder),
        "cartes": cartes,
    }
    return context


def changeDirectory(folder):
    prev_folder = folder
    print("Avant :", folder)
    recherche = search(r'^[(?:bouzzi)/]*(?P<newFolder>.*)$', folder)
    if recherche:
        folder = recherche.group('newFolder')
        print("Après :", folder)
    return folder


# ******************************  Views  ************************************

def accueil(request):
    return render(request, "bouzzi/accueil.html", {'subtitle': [SubtitleLink(text="Accueil")]})


@login_required(login_url='/bouzzi/connexion')
def index(request, folder="None"):
    folder = changeDirectory(folder)
    if folder == "":
        return accueil(request)
    else:
        return render(request, "bouzzi/index.html", carteur(folder))


def connexion(request):
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                nextPage = form.cleaned_data['nextPage']
                print("NEXT PAGE : ", nextPage)
                return redirect('index', folder=nextPage)
            else:
                error = True
                form = ConnexionForm(
                    initial={'nextPage': form.cleaned_data['nextPage']})
    elif request.GET and 'next' in request.GET and request.GET['next']:
        form = ConnexionForm(initial={'nextPage': request.GET['next']})
    else:
        form = ConnexionForm()

    return render(request, 'bouzzi/connexion.html', locals())


def deconnexion(request, folder):
    logout(request)
    return custom_redirect('connexion', next=folder)
