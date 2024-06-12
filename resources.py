from flask import Blueprint, request, jsonify, abort
from flask_restful import Api, Resource
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from . import db
from .models import User, Recipe
import json

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()

        # Check if the user already exists
        if User.query.filter_by(email=data['email']).first() is not None:
            return {'message': 'User with this email already exists'}, 400

        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {'message': 'An error occurred during registration', 'error': str(e)}, 500

        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'User registered successfully'
        }

        return response_data, 201
    

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user is None or not user.check_password(data['password']):
            return {'message': 'Invalid email or password'}, 401
        login_user(user)
        return {'message': 'Logged in successfully'}

class LogoutAPI(Resource):
    @login_required
    def post(self):
        if current_user.is_authenticated:  # Check if the user is logged in
            username = current_user.username
            email = current_user.email
            logout_user()
            return {'message': f'User {username} ({email}) logged out successfully'}, 200
        else:
            return {'error': 'User is already logged out'}, 400

class RecipeAPI(Resource):
    @login_required
    def get(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            abort(404, {'error': f'Recipe not found with id {recipe_id}'})
        
        return jsonify({
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'created_at': recipe.created_at,
            'user_id': recipe.user_id
        })

            

    @login_required
    def put(self, recipe_id):
        data = request.get_json()
        recipe = Recipe.query.get_or_404(recipe_id)
        if recipe.author != current_user:
            return jsonify({'message': 'You can only edit your own recipes'}), 403

        ingredients_str = json.dumps(data['ingredients'])
        recipe.title = data['title']
        recipe.description = data['description']
        recipe.ingredients = ingredients_str
        recipe.instructions = data['instructions']
        db.session.commit()
        return jsonify({'message': 'Recipe updated successfully'})

    @login_required
    def delete(self, recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        if recipe.author != current_user:
            return jsonify({'message': 'You can only delete your own recipes'}), 403

        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted successfully'})

class RecipeListAPI(Resource):
    @login_required
    def get(self):
        recipes = Recipe.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'created_at': recipe.created_at,
            'user_id': recipe.user_id
        } for recipe in recipes])

    @login_required
    def post(self):
        data = request.get_json()
        ingredients_str = '\n'.join(data['ingredients'])
        recipe = Recipe(
            title=data['title'],
            description=data['description'],
            ingredients=ingredients_str,
            instructions=data['instructions'],
            author=current_user
        )
        db.session.add(recipe)
        db.session.commit()
        response_data = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'created_at': recipe.created_at,
            'author': {
                'id': recipe.author.id,
                'username': recipe.author.username,
                'email': recipe.author.email
            }
        }

        return jsonify({'message': 'Recipe created successfully', 'recipe': response_data})
    
class RecipeSearchAPI(Resource):
    @login_required
    def get(self):
        query = request.args.get('q')
        if not query:
            return jsonify({'error': 'Search query parameter (q) is required'}), 400

        # Search for recipes by title or ingredients
        recipes = Recipe.query.filter(
            or_(Recipe.title.ilike(f'%{query}%'),
                Recipe.ingredients.ilike(f'%{query}%'))
        ).all()
        if not recipes:
            return {'message': f'No recipes found for the given search query ( {query} )'}, 404
        
        return jsonify([recipe.serialize() for recipe in recipes])
    


api.add_resource(RegisterAPI, '/register')
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RecipeListAPI, '/recipes')
api.add_resource(RecipeAPI, '/recipes/<int:recipe_id>')
api.add_resource(RecipeSearchAPI, '/recipes/search')
