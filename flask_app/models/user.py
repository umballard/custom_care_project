
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class User:
    db = "critters_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



  # Create Users Models
    @classmethod
    def create_user(cls,user_data):
        if not cls.validate_user(user_data):
            return False
        user_data = user_data.copy()
        user_data['password']  = bcrypt.generate_password_hash(user_data['password'])
        query = """
            INSERT INTO users
            (first_name, last_name, email, password)
            VALUES
            (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
            ;"""
        user_id = connectToMySQL(cls.db).query_db(query,user_data)
        session['user_id'] = user_id
        session['first_name'] = user_data['first_name']
        return user_id


    # Read Users Models
    @classmethod
    def get_user_by_email(cls,email):
        data = {'email' : email}
        query ="""
            SELECT * FROM
            users
            WHERE email = %(email)s
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            this_user = cls(results[0])
            return this_user
        return False


    #login
    @classmethod
    def login(cls,data):
        this_user = cls.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['first_name'] = this_user.first_name
                return True
        flash('Incorrect Login Information')
        return False
    
    #user_validations
    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        if len(data['email']) < 1:
            flash("Email Required")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash('account information exists in database, try again')
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if len(data['password']) < 8:
            flash("password must be at least 8 characters.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("passwords must match")
            is_valid = False
        print(is_valid)
        return is_valid