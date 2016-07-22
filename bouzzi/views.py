from django.http import Http404
from datetime import datetime
from django.shortcuts import render
from pathlib import Path
from . import models
import sys


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
    title = str
    onclic = str


class SubtitleLink:

    def __init__(self, text="", link=""):
        self.text = text
        self.link = link


def date_actuelle(request):
    return render(request, 'bouzzi/date.html', {'date': datetime.now()})


def addition(request, nombre1, nombre2):
    total = int(nombre1) + int(nombre2)

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'bouzzi/addition.html', locals())


def accueil(request):
    return render(request, "bouzzi/accueil.html", {'subtitle': [SubtitleLink(text="Accueil")]})


def subtitleur(folder):
    foldList = folder.split('/')
    subtitleList = []
    for i, sub in enumerate(foldList):
        subtitleList.append(SubtitleLink(
            text=sub, link='/'.join(foldList[:i + 1])))
    subtitleList.reverse()
    return subtitleList


def carteur(folder):
    if folder == 'None' or folder == "":
        return {'folder': "None", 'subtitle': [SubtitleLink(text='Index')], 'cartes': []}
    try:
        cartes = Dossier("bouzzi/links/" + folder).getBlocs()
    except FileNotFoundError:
        raise Http404(
            "FileNotFoundError : Ceci n'est pas un dossier valide : " + folder)
    except Exception:
        raise Http404(str(sys.exc_info()[0]))
    return {'folder': folder, 'subtitle': subtitleur(folder), "cartes": cartes}


def index(request, folder="None"):
    return render(request, "bouzzi/index.html", carteur(folder))
