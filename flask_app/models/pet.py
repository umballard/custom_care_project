
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Pet:
    db = "critters_schema" #which database are you using for this project
    def __init__(self, data):
        self.pet_id = data['pet_id']
        self.name = data['name']
        self.breed = data['breed']
        self.color = data['color']
        self.weight = data['weight']
        self.date_of_birth = data['date_of_birth']
        self.alerts = data['alerts']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.pet_owner = None



    # Create Pet Models

    @classmethod
    def add_pet(cls, data):
        if not cls.validate_pet(data):
            return False
        data = data.copy()
        data['users_id'] = session['users_id']
        print(data)
        query = """
            INSERT INTO pets 
            (name, breed, color, weight, date_of_birth, alerts, users_id)
            VALUES
            (%(name)s, %(breed)s, %(color)s, %(weight)s, %(date_of_birth)s, %(alerts)s, %(users_id)s)
            ;"""
        pet_service_id = connectToMySQL(cls.db).query_db(query,data)
        session['pet_id'] = pet_service_id
        print(pet_service_id)
        print(session)
        return pet_service_id
    
    # Read Pet Models

    @classmethod
    def get_all_pets_created_by_user(cls):
        users_id = session['users_id']
        query = """
            SELECT * FROM pets
            JOIN users on users.id = pets.users_id
            WHERE users_id = %(id)s
            ;"""
        data = {'id' : users_id }
        results = connectToMySQL(cls.db).query_db(query,data)
        all_owners_pets = []
        for result in results:
            one_pet = cls(result)
            one_pet_user_data = {
                'id' : result['id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'email' : result['email'],
                'password': result['password'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at'], 
            }
            pet_owner = user.User(one_pet_user_data)
            one_pet.pet_owner = pet_owner
            all_owners_pets.append(one_pet)
        return all_owners_pets
    
    @classmethod
    def get_pet_by_pet_id(cls, pet_id):
        query = """
            SELECT * FROM pets
            JOIN users on users.id = pets.users_id
            WHERE pet_id = %(id)s
            ;"""
        data = {'id' : pet_id }
        results = connectToMySQL(cls.db).query_db(query,data)
        return results[0]
    

    # Update Pet Models


    @classmethod
    def update_pet(cls,data):
        if not cls.validate_pet(data):
            return False
        data = {
            'pet_id' : data['pet_id'],
            'name' : data['name'],
            'breed' : data['breed'],
            'color' : data['color'],
            'weight': data['weight'],
            'date_of_birth' : data['date_of_birth'],
            'alerts' : data['alerts'],
            }
        query = """
            UPDATE pets
            SET
            name = %(name)s,
            breed = %(breed)s,
            color = %(color)s,
            weight = %(weight)s,
            date_of_birth = %(date_of_birth)s,
            alerts = %(alerts)s
            WHERE pet_id = %(pet_id)s
            ;"""
        print(data,query)
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Delete Pet Models
    @classmethod
    def delete_pet(cls,pet_id):
        # if session['users_id'] != cls.get_users_id_from_pet(pet_id):
        #     print(session,pet_id)
        #     return False
        data = {
                'id' : pet_id
            }
        query = """
            DELETE FROM pets
            WHERE pet_id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query,data)
        return True
    
    #pet_validations
    def validate_pet(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Name must be at least 2 characters")
            is_valid = False
        if len(data['breed']) < 2:
            flash("Breed must be at least 2 characters")
            is_valid = False
        if len(data['color']) < 2:
            flash("Color must be at least 2 characters")
            is_valid = False
        INT_REGEX = re.compile('^([1-9][0-9]?|100)$')
        if not INT_REGEX.search(data['weight']):
            flash("Must be at least 1lb")
            is_valid = False
        if len(data['alerts']) < 8:
            flash("Please enter alerts for staff to be aware of. Must be at least 8, but less than 250 charaters")
            is_valid = False
        if len(data['alerts']) > 250:
            flash("Please enter alerts for staff to be aware of. Must be at least 8, but less than 250 charaters")
            is_valid = False
        DATE_REGEX = re.compile('^\d{4}-\d{2}-\d{2}$')
        if not DATE_REGEX.match(data['date_of_birth']): 
            flash("Please provide your pets date of birth")
            is_valid = False
        return is_valid


