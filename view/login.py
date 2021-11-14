from flask import Blueprint, abort, jsonify, request, current_app

login_route = Blueprint('login', __name__)

@login_route.route('/callback', methods=['GET'])
def app_response_code():
    return '''  <script type="text/javascript">
                var token = window.location.href.split("access_token=")[1]; 
                window.location = "/callback_token/" + token;
            </script> '''

@login_route.route('/callback_token/<token>/', methods=['GET'])
def app_response_token(token):
    return jsonify({
        'token': token
    })
