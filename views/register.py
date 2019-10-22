from models.vets import Vets
from flask import render_template
from models.vets import Vets

def register_page():
    qs = Vets.filter()
    if qs:
        _vets_list = [u.__dict__ for u in qs]
        return render_template('register.html', vets_list=_vets_list)
