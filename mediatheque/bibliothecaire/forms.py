from django import forms
from .models import Media
from .models import Membre

class Creationmembre(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    tel = forms.FloatField(required=True)

class Creationmedia(forms.Form):
    name = forms.CharField(label='Nom', max_length=100)
    creator = forms.CharField(label='Réalisé par', max_length=100)
    type_media = forms.ChoiceField(label='Type de Média', choices=Media.TYPE_MEDIA)


class EmpruntForm(forms.Form):
    membre = forms.ModelChoiceField(queryset=Membre.objects.all(), label="Membre")
    media = forms.ModelChoiceField(queryset=Media.objects.filter(disponible=True, type_media__in=['livre', 'cd', 'dvd']), label="Média")