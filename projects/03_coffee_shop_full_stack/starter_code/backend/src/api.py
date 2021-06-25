import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    # Get data
    drinks = Drink.query.order_by(Drink.id).all()

    if len(drinks) == 0:
        abort(400)
    else:
        short_recipes = [drink.short() for drink in drinks]
        return jsonify({
            'success': True,
            'status': 200,
            'drinks': short_recipes
        })



'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    # Get data
    drinks = Drink.query.order_by(Drink.id).all()

    if len(drinks) == 0:
        abort(400)
    else:
        long_recipes = [drink.long() for drink in drinks]
        return jsonify({
            'success': True,
            'status': 200,
            'drinks': long_recipes
        })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()
    # Error handling with no data
    if body == {}:
        abort(400)

    # Get details of new drink from the request
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    # Check for unique name
    drink_check = Drink.query.filter(Drink.title == new_title).all()
    if len(drink_check) != 0:
        abort(400)

    try:
        # Create a new drink and insert it into the database
        new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        new_drink.insert()

        # return success message
        return jsonify({
            'success': True,
            'status': 200,
            'drinks': [new_drink.long()]
        })

    except:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):
    # Get drink data
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if drink:
        body = request.get_json()

        if body == {}:
            abort(400)
        # Get updated details of new drink from the request
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)
        # set drink details to the new values
        if new_title:
            drink.title = new_title
        if new_recipe:
            drink.recipe = new_recipe
        # update drink
        try:    
            drink.update()

            # Return success message
            return jsonify({
                'success': True,
                'status': 200,
                'drinks': [drink.long()]
            })
        except:
            abort(422)

    else:
        # No drink found
        abort(404)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    # See if drink exists
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if drink:
        try:
            drink.delete()

            # Return success message
            return jsonify({
                'success': True,
                'status': 200,
                'delete': drink.id
            })
        except:
            abort(422)

    else:
        # No drink found
        abort(404)



# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code