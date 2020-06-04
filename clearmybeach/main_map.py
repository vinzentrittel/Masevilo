from flask import Blueprint

def create_blueprint():
    map_bp = Blueprint('map', __name__, url_prefix='/map')

    @map_bp.route('/')
    def index():
        return 'Main view'

    return map_bp
