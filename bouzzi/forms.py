from django import forms


class ConnexionForm(forms.Form):

    username = forms.CharField(label="Nom d'utilisateur", max_length=50, widget=forms.TextInput(attrs={
                               'class': 'mdl-textfield__input'}))
    password = forms.CharField(
        label="Mot de passe", widget=forms.PasswordInput(attrs={
            'class': 'mdl-textfield__input'}))
    nextPage = forms.CharField(
        widget=forms.HiddenInput(), initial='/bouzzi/')
