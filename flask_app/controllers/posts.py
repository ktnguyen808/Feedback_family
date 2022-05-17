from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.post import Tree
from flask_app.models.user import User


@app.route('/new/tree')
def new_tree():
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['users_id']
    }
    return render_template('new_tree.html',user=User.get_by_id(data))


@app.route('/plant/tree',methods=['POST'])
def plant_tree():
    if 'users_id' not in session:
        return redirect('/logout')
    if not Tree.validate_tree(request.form):
        return redirect('/new/tree')
    data = {
        "species": request.form["species"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date_planted": request.form["date_planted"],
        "users_id": session["users_id"]
    }
    Tree.save(data)
    return redirect('/dashboard')

@app.route('/edit/tree/<int:id>')
def edit_tree(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['users_id']
    }
    return render_template("edit_info.html",edit=Tree.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/tree',methods=['POST'])
def update_tree():
    if 'users_id' not in session:
        return redirect('/logout')
    if not Tree.validate_tree(request.form):
        return redirect('/new/tree')
    data = {
        "species": request.form["species"],
        "reason": request.form["reason"],
        "location": request.form["location"],
        "date_planted": request.form["date_planted"],
        "id": request.form['id']
    }
    Tree.update(data)
    return redirect('/dashboard')

@app.route('/show/tree/<int:id>')
def show_tree(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['users_id']
    }
    return render_template("show_tree.html",tree=Tree.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/tree/<int:id>')
def destroy_tree(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Tree.destroy(data)
    return redirect('/dashboard')