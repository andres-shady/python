from django.shortcuts import render
from bibliothecaire.models import Media

# Create your views here.
def list_media_view(request):
    medias = Media.objects.all()
    return render(request, 'mediatheque/list_media_membre.html', {'medias': medias})