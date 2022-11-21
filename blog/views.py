from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement

def post_list(request):
    animals = Animal.objects.all()
    equipement = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'animals': animals, 'equipement': equipement})

def match_status_place(animal_etat, nouveau_lieu_name):
    # Case Mangeoire
    if animal_etat == "affamé" and nouveau_lieu_name == "mangeoire":
        return True
    # Case Roue
    elif animal_etat == "repus" and nouveau_lieu_name == "roue":
        return True
    # Case Litiere
    elif animal_etat == "endormi" and nouveau_lieu_name == "litière":
        return True
    # Case Nid
    elif animal_etat == "fatigué" and nouveau_lieu_name == "nid":
        return True
    # Other case 
    else:
        return False

def update_availability(place):
    if place.id_equip == "litière":
        place.disponibilite = "libre"
    elif place.id_equip in ["roue", "mangeoire", "nid"]:
        place.disponibilite = "occupé"
    place.save()

def update_status(animal, place):
    # Case Mangeoire
    if place.id_equip == "mangeoire":
        animal.etat = "repus"
    # Case Roue
    elif place.id_equip == "roue":
        animal.etat = "fatigué"
    #Case Litiere
    elif place.id_equip == "litière":
        animal.etat = "affamé"
    # Case Nid
    elif place.id_equip == "nid":
        animal.etat = "endormi"
    animal.save()


def post_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    message = ""
    error = None
    form = MoveForm(request.POST, instance=animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    if request.method == "POST" and form.is_valid():
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip) 
        # Case correct
        if nouveau_lieu.disponibilite == "libre" and match_status_place(animal.etat, nouveau_lieu.id_equip):
            error = False
            ancien_lieu.disponibilite = "libre"
            update_availability(nouveau_lieu)
            ancien_lieu.save()
            form.save() 
            update_status(animal, nouveau_lieu)
            message = "La modification a été réalisée avec succès"
        # Case error
        else:
            message = "C'est pas posible de faire la modification"
            error = True
        return render(request,
                  'blog/post_detail.html',
                  {'animal': animal, 'message': message, 'error': error, 'lieu': ancien_lieu, 'new_lieu':nouveau_lieu, 'form': form})
    else:
        form = MoveForm()
        return render(request,
                  'blog/post_detail.html',
                  {'animal': animal, 'message': message, 'lieu': ancien_lieu, 'form': form})