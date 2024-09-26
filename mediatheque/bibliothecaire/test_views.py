import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from bibliothecaire.models import Membre, Media
from django.utils import timezone
from datetime import timedelta

@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(username='bibliothecaire', password='mediatheque')

@pytest.fixture
def client():
    return Client()

#Test membres
@pytest.mark.django_db
def test_home_view(superuser, client):
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('bibliothecaire_home')
    response = client.get(url)
    assert response.status_code == 200
    assert "Bienvenue, sur le menu des bibliothecaires"

@pytest.mark.django_db
def test_list_membre_view(superuser, client):
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('list_membres')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_membre_view(superuser, client):
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('add_membre')
    data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@gmail.com',
        'tel': '0123456789',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Membre.objects.filter(first_name='Jane').exists()
    assert Membre.objects.filter(last_name='Doe').exists()
 
@pytest.mark.django_db
def test_membre_detail_view(superuser, client):
    membre = Membre.objects.create(first_name='Elodie', last_name='Champ', email='e.champ@gmail.com', tel= '1234567890')
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('membre_detail', args=[membre.id])
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_updatemembres_view(superuser, client):
    membre = Membre.objects.create(first_name='Lucas', last_name='Coen', email='lucas.coen@gmail.com', tel= '1234567890')
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('update_membre', args=[membre.id])
    response = client.post(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_updatemembres_view(superuser, client):
    membre = Membre.objects.create(first_name='Lucas', last_name='Coen', email='lucas.coen@gmail.com', tel= '1234567890')
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('delete_membre', args=[membre.id])
    response = client.post(url)
    assert response.status_code == 302

#Test media

@pytest.mark.django_db
def test_add_media_view(superuser, client):
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('add_media')
    data = {
        'name': 'Livre 1',
        'creator': 'Auteur 1',
        'type_media': 'livre',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Media.objects.filter(name='Livre 1').exists()

@pytest.mark.django_db
def test_list_media_view(superuser, client):
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('list_media')
    response = client.get(url)
    assert response.status_code == 200

#Partie emprunt

@pytest.mark.django_db
def test_add_emprutn_view(superuser, client):
    client.login(username='bibliothecaire', password='mediatheque')
    membre = Membre.objects.create(first_name='Lucas', last_name='Coen', email='lucas.coen@gmail.com', tel= '1234567890')
    media = Media.objects.create(name='Livre 1', creator='Auteur 1', type_media='livre', disponible=True)
    url = reverse('add_emprunt')
    data = {
        'membre': membre.id,
        'media': media.id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    media.refresh_from_db()
    assert media.emprunteur == membre
    assert media.disponible == False

@pytest.mark.django_db
def test_list_emprunt_view(superuser, client):
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('list_emprunt')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_return_emprunt_view(superuser, client):
    membre = Membre.objects.create(first_name='Lucas', last_name='Coen', email='lucas.coen@gmail.com', tel= '1234567890')
    media = Media.objects.create(name='Livre 1', creator='Auteur 1', type_media='livre', disponible=True)
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('return_emprunt', args=[media.id])
    response = client.post(url)
    assert response.status_code == 302
    media.refresh_from_db()
    assert media.emprunteur == None
    assert media.disponible == True

@pytest.mark.django_db
def test_erreur_view(superuser, client):
    client.login(username='bibliothecaire', password='mediatheque')
    url = reverse('erreur_emprunt')
    response = client.get(url)
    assert response.status_code == 200
