from flask import render_template, request, flash, url_for, redirect

from models.vets import Vets


def owner_register():
    headers = request.headers
    cookie = headers.get("Cookie")
    if not cookie.__contains__("remember_token"):
        flash("You have not logged in!")
        return home_page()
    qs = Vets.filter()
    if qs:
        _vets_list = [u.__dict__ for u in qs]
        return render_template('owner_register.html', vets_list=_vets_list)


def vet_register():
    headers = request.headers
    cookie = headers.get("Cookie")
    if not cookie.__contains__("remember_token"):
        flash("You have not logged in!")
        return home_page()
    return render_template('vet_register.html')


def home_page():
    return render_template('base.html')
