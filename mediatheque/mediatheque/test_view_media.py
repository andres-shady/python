import pytest
from django.urls import reverse
from django.test import Client
from bibliothecaire.models import Media

@pytest.mark.django_db
def test_list_media_view():
    media1 = Media.objects.create(name="Livre 1", creator="Auteur 1", type_media="livre", disponible=True)
    media2 = Media.objects.create(name="CD 1", creator="Artiste 1", type_media="cd", disponible=True)
    client = Client()
    url = reverse('list_media_membre')
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode('utf-8')
    assert "Livre 1" in content
    assert "Auteur 1" in content
    assert "CD 1" in content
    assert "Artiste 1" in content