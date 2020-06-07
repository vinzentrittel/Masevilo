from flask import Blueprint, render_template

def create_blueprint():
    map_bp = Blueprint('map', __name__, url_prefix='/map')

    @map_bp.route('/')
    def index():
        return render_template('map.html')

    return map_bp
