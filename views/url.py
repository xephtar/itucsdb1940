from flask import render_template, request, flash

from models.owners import Owners
from models.vets import Vets
from models.vets_to_owners import Vets_to_Owners


def owner_register():
    headers = request.headers
    cookie = headers.get("Cookie")
    if not cookie.__contains__("remember_token"):
        flash("You have not logged in!")
        return home_page()
    return render_template('owner_register.html')


def vet_register():
    headers = request.headers
    cookie = headers.get("Cookie")
    if not cookie.__contains__("remember_token"):
        flash("You have not logged in!")
        return home_page()
    return render_template('vet_register.html')


def vet_profile(id):
    v = Vets.get(id=id)
    return render_template('vet_profile.html', vet=v)


def vet_profiles():
    v = Vets.filter()
    return render_template('vet_profiles.html', vets=v)


def relations():
    r = Vets_to_Owners.filter()
    return render_template('relations.html', relations=r)


def owner_profile(phonenumber):
    o = Owners.get(phonenumber=phonenumber)
    _vets = Vets.filter()
    return render_template('owner_profile.html', owner=o, vet_list=_vets)


def owner_profiles():
    o = Owners.filter()
    return render_template('owner_profiles.html', owners=o)


def home_page():
    return render_template('base.html')
