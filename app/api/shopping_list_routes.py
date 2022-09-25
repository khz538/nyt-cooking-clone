from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Ingredient, ShoppingList, ingredient
from .auth_routes import validation_errors_to_error_messages

shopping_list_routes = Blueprint('shopping_list', __name__)

# Add all recipe ingredients to shopping list
@shopping_list_routes.route('/add/', methods=['POST'])
@login_required
def add_to_shopping_list():
    recipe_id = request.json['recipe_id']
    ingredients = db.session.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).all()
    shopping_list = db.session.query(ShoppingList).filter(ShoppingList.user_id == current_user.id).all()
    print('shopping_list:', shopping_list)
    if ingredients is None:
        return {'errors': ['Ingredients not found']}, 404
    else:
        if len(shopping_list) > 0:
            res1 = []
            new_shopping_list = db.session.query(ShoppingList).filter(ShoppingList.user_id == current_user.id).all()
            new_shopping_list_dict = [i.to_dict() for i in new_shopping_list]
            for ingredient in ingredients:
                if ingredient not in new_shopping_list:
                    res1.append(ingredient)
            print('res1:', res1)
            return jsonify(res1)
        if len(shopping_list) == 0:
            res2 = []
            for ingredient in ingredients:
                shopping_list_item = ShoppingList(
                    user_id=current_user.id,
                    ingredient_id=ingredient.id
                )
                db.session.add(shopping_list_item)
                db.session.commit()
                res2.append(shopping_list_item.to_dict())
            print('res2:', res2)
            return jsonify(res2)
