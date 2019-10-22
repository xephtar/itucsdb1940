from models.vets import Vets
from flask import render_template


def register_page():
    u = Vets.get(id=id)
    if u:
        vets_list = u.__dict__
    return render_template("register.html", vets_list=sorted(vets_list))