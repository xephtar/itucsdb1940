from models.vets import Vets
from flask import render_template


def register_page():
    html = """
            {% block title %}Movie list{% endblock %}
        {% block content %}
            <h1 class="title">Movies</h1>
        
            {% if vets_list %}
            <table class="table is-striped is-fullwidth">
              {% for id, vet in vets_list %}
              <tr>
                <td>
                  {{ vet.name }}
                  {% if vet.age %} ({{ vet.age }}) {% endif %}
                </td>
              </tr>
              {% endfor %}
            <select name="vets">
                {% for id, vet in vets_list %}
                    <option value="{{ id }}">{{ vet }}</option>
                {% endfor %}
            </select>
            </table>
            {% endif %}
        {% endblock %}
    """
    v = Vets.get(id=id)
    if v:
        _vets_list = v.__dict__
        return render_template(html, vets_list=sorted(_vets_list))
