from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)
DATA_FILE = "recipes.json"

def load_recipes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_recipes(recipes):
    with open(DATA_FILE, "w") as file:
        json.dump(recipes, file, indent=4)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    data = request.json
    name = data.get("name")
    ingredients = data.get("ingredients")
    instructions = data.get("instructions")
    category = data.get("category")
    
    recipes = load_recipes()
    recipes.append({"name": name, "ingredients": ingredients, "instructions": instructions, "category": category})
    save_recipes(recipes)
    return jsonify({"message": "Recipe added successfully!"})

@app.route("/search_recipe", methods=["GET"])
def search_recipe():
    search_type = request.args.get("type")
    query = request.args.get("query").lower()
    recipes = load_recipes()

    results = []
    for recipe in recipes:
        if search_type == "ingredient" and query in [i.lower() for i in recipe["ingredients"]]:
            results.append(recipe)
        elif search_type == "category" and query == recipe["category"].lower():
            results.append(recipe)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
