import pytest
from django.utils import timezone
from datetime import timedelta
from .models import Membre, Media


@pytest.mark.django_db
def test_create_membre():
    membre = Membre.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        tel="1234567890",
    )


    assert membre.first_name == "John"
    assert membre.last_name == "Doe"
    assert membre.email == "john.doe@example.com"
    assert membre.tel == "1234567890"


@pytest.mark.django_db
def test_membre_peut_emprunter():
    membre = Membre.objects.create(
        first_name="Bob",
        last_name="Dylan",
        email="bob.dylan@example.com",
        tel="1234567890",
        bloque=False,
    )

    assert membre.peut_emprunter() is True

    #Emprunt du 4eme media
    Media.objects.create(name='Livre 1', creator='Auteur 1', type_media='livre', emprunteur=membre, dateEmprunt=timezone.now()-timedelta(days=3))
    Media.objects.create(name='Cd 2', creator='compositeur 1', type_media='cd', emprunteur=membre, dateEmprunt=timezone.now()-timedelta(days=1))
    Media.objects.create(name='Livre 2', creator='Auteur 2', type_media='livre', emprunteur=membre, dateEmprunt=timezone.now()-timedelta(days=2))
    Media.objects.create(name='Livre 3', creator='Auteur 3', type_media='livre', emprunteur=membre, dateEmprunt=None)

    assert membre.peut_emprunter() is False

    #Emprunt de media avec un média emprunter il y a 2 semaines
    Media.objects.create(name='Livre 1', creator='Auteur 1', type_media='livre', emprunteur=membre, dateEmprunt=timezone.now()-timedelta(weeks=2))

    assert membre.peut_emprunter() is False

@pytest.mark.django_db
def test_membre_str_method():
    membre = Membre.objects.create(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        tel="1234567890",
    )

    assert str(membre) == 'Jane Doe'

@pytest.mark.django_db
def test_creation_media():

    membre = Membre.objects.create(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        tel="1234567890",
    )

    media = Media.objects.create(
        name='Hunger Games',
        creator='Suzanne Collin',
        type_media='livre',
        disponible=True,
        dateEmprunt=timezone.now(),
        emprunteur=membre,
    )


    assert media.name == 'Hunger Games'
    assert media.creator == 'Suzanne Collin'
    assert media.type_media == "livre"
    assert media.disponible == True
    assert media.emprunteur == membre

@pytest.mark.django_db
def test_media_str_method():

    media = Media.objects.create(
        name='Hunger Games',
        creator='Suzanne Collin',
        type_media='dvd',
        disponible=True,
        dateEmprunt=timezone.now(),
    )

    assert str(media) == "Hunger Games (DVD)"


@pytest.mark.django_db
def test_media_est_disponible():
    media = Media.objects.create(
        name='Le seigneur des anneaux',
        creator='J.k.k Tolkien',
        type_media='livre',
        disponible=True,
        dateEmprunt=None,
    )

    assert media.est_disponible() is True

    media.dateEmprunt = timezone.now()
    media.save()

    assert media.est_disponible() is False

    #Empunt d'un jeu de plateau
    media.type_media = "Jeu_de_plateau"
    media.dateEmprunt = None
    media.save()

    assert media.est_disponible() is False