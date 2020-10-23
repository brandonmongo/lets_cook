import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGODB_NAME"] = os.environ.get("MONGODB_NAME")
app.secret_key = os.environ.get("SERCET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/all_recipes")
def all_recipes():
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the user exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("user")})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for('register'))

        user = {
            "username": request.form.get("user"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(user)

        # inter new session into cookie
        session["current_user"] = request.form.get("user")
        flash("Registration complete")
        return redirect(url_for("profile", username=session["current_user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username is in the mongoDB database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("user")})

        if existing_user:
            # check if password matches
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["current_user"] = request.form.get("user")
                flash("Hello, {}".format(request.form.get("user")))
                return redirect(
                    url_for("profile", username=session["current_user"]))
            else:
                # if password is invaild
                flash("Incorrect Username/Password")
                return redirect(url_for("login"))

        else:
            # if username is invaild
            flash("Incorrect Username/Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["current_user"]})["username"]

    if session["current_user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove cookie user
    flash("You been logged out")
    session.pop("current_user")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        vegetarian = "yes" if request.form.get("vegetarian") else "no"
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "tools": request.form.getlist("tools[]"),
            "ingredients": request.form.getlist("ingredients[]"),
            "preparation": request.form.getlist("preparation[]"),
            "serving": request.form.get("serving"),
            "difficulty": request.form.get("difficulty"),
            "vegetarian": vegetarian,
            "added_by": session["current_user"]
        }
        print(request.form.getlist("ingredients[]"))
        mongo.db.recipes.insert_one(recipe)
        recipes = mongo.db.recipes.find()
        return render_template("recipes.html", recipes=recipes)
    return render_template("add_recipe.html")


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    viewed_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    return render_template("view_recipe.html", viewed_recipe=viewed_recipe)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        vegetarian = "yes" if request.form.get("vegetarian") else "no"
        edited_recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "tools": request.form.getlist("tools[]"),
            "ingredients": request.form.getlist("ingredients[]"),
            "preparation": request.form.getlist("preparation[]"),
            "serving": request.form.get("serving"),
            "difficulty": request.form.get("difficulty"),
            "vegetarian": vegetarian,
            "added_by": session["current_user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, edited_recipe)
        flash("Recipe Successfully Edited")
        return redirect(url_for("all_recipes"))

    viewed_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("edit_recipe.html", viewed_recipe=viewed_recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
