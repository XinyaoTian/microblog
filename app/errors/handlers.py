from flask import render_template, request
# from app import app, db
from app import db
# import bp for decorator
from app.errors import bp
from app.api.errors import error_response as api_error_response


# judge to reply in HTML or JSON preference
def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    # needs a json format
    if wants_json_response():
        return api_error_response(404)
    # return html format
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    # return json format
    if wants_json_response():
        return api_error_response(500)
    # return html format
    return render_template('errors/500.html'), 500
