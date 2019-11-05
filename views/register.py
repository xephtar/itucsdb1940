from flask import render_template
from models.vets import Vets


def list_vets():
    qs = Vets.filter()
    if qs:
        _vets_list = [u.__dict__ for u in qs]
        return render_template('owner_register.html', vets_list=_vets_list)


def vet_register():
    return render_template('vet_register.html')
