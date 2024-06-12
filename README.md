# Recipe App

This is a Flask-based web application for managing and sharing recipes.

## Overview

The Recipe App allows users to register, log in, and manage their own recipes. Users can create, view, update, and delete recipes. Additionally, users can search for recipes by title or ingredients.

## Endpoints

- `POST /api/register`: Register a new user.
- `POST /api/login`: Log in an existing user.
- `POST /api/logout`: Log out the current user.
- `GET /api/recipes`: Get all recipes of the currently logged-in user.
- `POST /api/recipes`: Create a new recipe.
- `GET /api/recipes/<recipe_id>`: Get details of a specific recipe.
- `PUT /api/recipes/<recipe_id>`: Update details of a specific recipe.
- `DELETE /api/recipes/<recipe_id>`: Delete a specific recipe.
- `GET /api/recipes/search?q=<query>`: Search for recipes by title or ingredients.

## Setup Instructions

1. Clone the repository:
git clone https://github.com/your-username/recipe-app.git

2. Navigate to the project directory:

3. Install dependencies:

4. Set up the database:
   flask db init
  flask db migrate
  flask db upgrade
5. Run the Flask application:
flask run
