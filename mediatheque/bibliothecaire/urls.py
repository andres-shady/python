from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bibliothecaire_home'),
    path('membre/list', views.list_membre_view, name='list_membres'),
    path('membre/add_membre', views.add_membre_view, name='add_membre'),
    path('membre/<int:id>', views.membre_detail_view, name='membre_detail'),
    path('membre/<int:id>/update_membre', views.updatemembres_view, name='update_membre'),
    path('membre/<int:id>/delete', views.deletemembre_view, name='delete_membre'),
    path('media/add_media', views.add_media_view, name='add_media'),
    path('media/list_media', views.list_media_view, name='list_media'),
    path('emprunt/add_emprunt', views.add_emprunt_view, name='add_emprunt'),
    path('emprunt/list_emprunt', views.list_emprunt_view, name='list_emprunt'),
    path('media/<int:id>/return/', views.return_emprunt_view, name='return_emprunt'),
    path('emprunt/erreur', views.erreur_view, name='erreur_emprunt'),
]