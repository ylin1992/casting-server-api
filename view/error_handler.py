from flask import Blueprint, jsonify

error_handler = Blueprint('error_handler', __name__)

# use "app_errorhandler" instead of "errorhandler" 
# to listen app-level errors
# reference: https://github.com/pallets/flask/issues/3572#issuecomment-613575568

@error_handler.app_errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400

@error_handler.app_errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404

@error_handler.app_errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@error_handler.app_errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal error'
    }), 500

@error_handler.app_errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401
    
@error_handler.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

# @app.errorhandler(AuthError)
# def process_AuthError(error):
#     res = jsonify(error.error)
#     res.status_code = error.status_code

#     return res