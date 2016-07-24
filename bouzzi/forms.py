from django import forms


class ConnexionForm(forms.Form):

    username = forms.CharField(label="Nom d'utilisateur", max_length=50)
    password = forms.CharField(
        label="Mot de passe", widget=forms.PasswordInput)
    nextPage = forms.CharField(
        widget=forms.HiddenInput(), initial='/bouzzi/')
