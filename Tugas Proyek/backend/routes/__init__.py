from flask import Blueprint

bp = Blueprint('main', __name__)

from . import user_routes, detail_kos_routes, gallery_routes, review_routes, admin_routes
