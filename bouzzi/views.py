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

# ***********************  Data  ***************************************

IMG = [ 'png' , 'jpg' , 'gif' ]
COMMENT = "Fichier : {fichier} Extension : {extension}"
ID_BLOC = "idBloc_"
STYLE = """#{id} \{ {propriete} \}"""

# ***********************  Traitement de données  ************************


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


class Dossier:

    def __init__(self, folder=''):
        self.folder = folder
        self.path_obj = Path(folder)
        self.iterdir = self.path_obj.iterdir

    def getFiles(self):
        return [file for file in self.iterdir()]

    def getBlocs(self):
        blocList = []
        for fichier in self.getFiles():
            bloc = Bloc(Fichier)
            bloc.calculer()
            blocList.append(bloc)
        return blocList
     
    def subtitleur(self):
        foldList = self.folder.split('/')
        subtitleList = []
        for i, sub in enumerate(foldList):
            subtitleList.append(SubtitleLink(
                text=sub, link='/'.join(foldList[:i + 1])))
        subtitleList.reverse()
        return subtitleList
    
    def getContext(self):
        context = {
            'folder' : self.folder,
            'subtitles' : self.subtitleur(),
            'cartes' : self.getBlocs()
            }
        return context
        
        
class Bloc:

    def __init__(self, fichier=""):
        self.fichier = fichier # fichier est normalement de type Path 
        #calcul du nom de fichier
        self.nomFichier = str(fichier).split('/')[-1]
        #calcul de l'extension
        if '.' in self.nomFichier :
            self.extension = self.nomFichier.split('.')[-1]
        else :
            self.extension = ""
        #calcul de l'id
        self.id_css = ID_BLOC + "_".join(self.nomFichier.split())
        #mise par défaut des autres paramètres
        self.title = ""
        self.commentaire = ""
        self.actions = ""
        self.hasCommentaire = False
        self.hasActions = False
        self.style= ""
        
    def calculer(self):
        self.calcStyle()
        self.calcCommentaire()
        self.calcAction()
        self.calcTitle()
        
    def calcStyle(self):
        sefl.style=""
        if self.extension in IMG:
            style = """#{id} \{ {propriete} \}""".format(id=self.id_css, propriete="background: red;")
            self.style += style
    
    def calcCommentaire(self):
        self.commentaire = COMMENT.format(fichier = str(self.fichier), extension = self.extension)
        self.hasCommentaire = True
        
    def calcTitle(self):
        self.title = self.nomFichier
        
    def calcAction(self):
        self.hasActions = False
        self.actions = []
        if self.fichier.is_dir() :
            title = "OPEN"
            onclic = 'href="' + str(self.fichier) + '" '
            self.actions.append(Action(title=title, onclic=onclic))
            self.hasActions = True

class Action:

    def __init__(self, title="", onclic=""):
        self.title = title
        self.onclic = onclic


class SubtitleLink:

    def __init__(self, text="", link=""):
        self.text = text
        self.link = link


def carteur(folder):
    if folder == 'None' or folder == "" or folder == "deconnexion":
        return {'folder': "None", 'subtitle': [SubtitleLink(text='Index')], 'cartes': []}
    try:
        directory = Dossier("bouzzi/links/" + folder)
        context = directory.getContext()
    except FileNotFoundError:
        raise Http404(
            "FileNotFoundError : Ceci n'est pas un dossier valide : " + folder)
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
    loginError = False
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
                loginError = True
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
