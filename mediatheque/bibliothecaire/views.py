from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .forms import Creationmembre
from .forms import Creationmedia
from .forms import EmpruntForm
from .models import Membre
from .models import Media

def is_superuser(user):
    return user.is_superuser
#username: bibliothecaire
#password: mediatheque

@login_required
@user_passes_test(is_superuser)
def home(request):
    return render(request, 'bibliothecaire/home.html')

#Partie Membre
@login_required
@user_passes_test(is_superuser)
def list_membre_view(request):
    membres = Membre.objects.all()
    return render(request, 'bibliothecaire/list_membre.html', {'membres': membres})

@login_required
@user_passes_test(is_superuser)
def add_membre_view(request):
    if request.method == 'POST':
        creationmembre = Creationmembre(request.POST)
        if creationmembre.is_valid():
            membre = Membre()
            membre.first_name = creationmembre.cleaned_data['first_name']
            membre.last_name = creationmembre.cleaned_data['last_name']
            membre.email = creationmembre.cleaned_data['email']
            membre.tel = creationmembre.cleaned_data['tel']
            membre.save()
            membres = Membre.objects.all()
            return redirect('membre_detail', id=membre.id)
    else:
        creationmembre = Creationmembre()
        return render(request, 'bibliothecaire/add_membre.html', {'creationMembre': creationmembre})


@login_required
@user_passes_test(is_superuser)
def membre_detail_view(request, id):
    membre = get_object_or_404(Membre, id=id)
    return render(request, 'bibliothecaire/membre_detail.html', {'membre': membre})

@login_required
@user_passes_test(is_superuser)
def updatemembres_view(request, id):
    membre = get_object_or_404(Membre, id=id)
    if request.method == 'POST':
        form = Creationmembre(request.POST)
        if form.is_valid():
            membre.first_name = form.cleaned_data['first_name']
            membre.last_name = form.cleaned_data['last_name']
            membre.email = form.cleaned_data['email']
            membre.tel = form.cleaned_data['tel']
            membre.save()
            membres = Membre.objects.all()
            return redirect('membre_detail', id=membre.id)
    else:
        form = Creationmembre(initial={
            'first_name': membre.first_name,
            'last_name': membre.last_name,
            'email': membre.email,
            'tel': membre.tel,
        })
    return render(request, 'bibliothecaire/update_membre.html', {'form': form, 'membre': membre})

@login_required
@user_passes_test(is_superuser)
def deletemembre_view(request, id):
    membre = get_object_or_404(Membre, id=id)
    if request.method == 'POST':
        membre.delete()
        return redirect('list_membres')
    return render(request, 'bibliothecaire/delete_membre.html', {'membre': membre})


#Partie Media
@login_required
@user_passes_test(is_superuser)
def add_media_view(request):
    if request.method == 'POST':
        form = Creationmedia(request.POST)
        if form.is_valid():
            media = Media(
                name=form.cleaned_data['name'],
                creator=form.cleaned_data['creator'],
                type_media=form.cleaned_data['type_media']
            )
            media.save()
            return redirect('bibliothecaire_home')
    else:
        form = Creationmedia()
    return render(request, 'bibliothecaire/add_media.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def list_media_view(request):
    medias = Media.objects.all()
    return render(request, 'bibliothecaire/list_media.html', {'medias': medias})


#Partie Emprunt

@login_required
@user_passes_test(is_superuser)
def add_emprunt_view(request):
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            membre = form.cleaned_data['membre']
            media = form.cleaned_data['media']

            if media.est_disponible() and membre.peut_emprunter():
                media.dateEmprunt = timezone.now()
                media.emprunteur = membre
                media.disponible = False
                media.save()
                return redirect('list_media')
            else:
                if not media.est_disponible():
                    messages.error(request, "Ce média n'est pas disponible pour l'emprunt.")
                if not membre.peut_emprunter():
                    messages.error(request, "Ce membre ne peut pas emprunter de médias (trop d'emprunts ou des emprunts en retard).")
                return redirect('erreur_emprunt')
    else:
        form = EmpruntForm()
        return render(request, 'bibliothecaire/emprunt_media.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def list_emprunt_view(request):
    emprunts = Media.objects.filter(disponible=False)
    emprunts_par_type = {
        type_media[1]: emprunts.filter(type_media=type_media[0])
        for type_media in Media.TYPE_MEDIA
    }
    return render(request, 'bibliothecaire/list_emprunt.html', {'emprunts_par_type': emprunts_par_type})


@login_required
@user_passes_test(is_superuser)
def return_emprunt_view(request, id):
    media = get_object_or_404(Media, id=id)
    if request.method == 'POST':
        media.disponible = True
        media.dateEmprunt = None
        media.emprunteur = None
        media.save()
        return redirect('list_emprunt')
    return render(request, 'bibliothecaire/return_emprunt.html', {'media': media})


@login_required
@user_passes_test(is_superuser)
def erreur_view(request):
    return render(request, 'bibliothecaire/erreur_emprunt.html')