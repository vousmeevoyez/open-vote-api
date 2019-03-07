"""
    Static Routes
"""
from flask import send_from_directory
from flask import current_app
from flask_restplus import Resource

from app.api.static import api

# flask rest plus extesnion

@api.route("/images/<filename>")
class ImageStaticRoutes(Resource):
    """
        Image routes
        api/v1/static/images
    """
    def get(self, filename):
        return send_from_directory(current_app.config["UPLOAD_FOLDER"],
                                   filename)
