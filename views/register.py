from models.vets import Vets
from flask import render_template


def register_page():
    v = Vets.get(id=id)
    if v:
        _vets_list = v.__dict__
        return render_template('register.html', vets_list=sorted(_vets_list))
