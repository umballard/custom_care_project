from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import pet

# import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request


# Create Users Controller

@app.route('/add_pet', methods = ['GET', 'POST'])
def create_pet():
    if 'users_id' not in session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('add_pet.html')
    
    if request.method == 'POST':
        if pet.Pet.add_pet(request.form):
            return redirect ('/dashboard')
    return redirect('/add_pet')


# Read Users Controller

@app.route('/view_pet/<int:pet_id>')
def show_pet(pet_id):
    if 'users_id' not in session:
        return redirect('/')
    pet_info = pet.Pet.get_pet_by_pet_id(pet_id)
    if pet_info['users_id'] != session['users_id']:
        return redirect('/')
    return render_template('view_pet.html',pet_info = pet_info)

# need if statement to protect against error if viewing pet with no services(tuple index out of range)

# # Update Users Controller

@app.route('/update_pet', methods=['POST'])
def update_pet():
        if 'users_id' not in session:
            return redirect('/')
        if pet.Pet.update_pet(request.form):
            return redirect(f'/view_pet/{request.form["pet_id"]}')
        return redirect(f'/view_pet/{request.form["pet_id"]}')

# Delete Users Controller

@app.route('/dashboard/delete/<int:pet_id>')
def delete_pet(pet_id):
    if 'users_id' not in session: 
        return redirect('/')
    pet.Pet.delete_pet(pet_id)
    return redirect('/dashboard')

# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.