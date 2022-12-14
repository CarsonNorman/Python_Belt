from flask_app import bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, render_template as render, redirect, request, session, flash, url_for
from flask_app.models.user_model import User
import re

db = 'beltdb'
class Login:
    def __init__(self, data):
        self.id = data.id
        self.email = data.email
        self.first_name = data.first_name
        self.last_name = data.last_name
        self.password = data.password
        self.created_at = data.created_at
        self.updated_at = data.updated_at

    @classmethod
    def create(cls, data):
        results = User.create(data)
        if results:
            session['id'] = results
            return redirect(url_for('renderHome', id=results))
        else:
            flash('Please login with existing account', 'create')
            return redirect(url_for('landing'))

    @classmethod
    def login(cls, data):
        print('data',data)
        query="""
        SELECT *
        FROM users 
        WHERE email=%(email)s
        """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if not results:
            flash('Login invalid', 'login')
            return redirect(url_for('landing'))
        for result in results:
            userPass = data['pass']
            checkPass = result['password']
            if not bcrypt.check_password_hash(checkPass, userPass):
                flash('Login invalid', 'login')
                return redirect(url_for('landing'))
            session['id'] = result['id']
            return redirect(url_for('renderHome'))
        

    @staticmethod
    def logout():
        session.clear()
        return redirect('/')
    
    @staticmethod
    def ValidateUserCreate(data):
        passEx = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        emailEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if data['email'] == '' or not emailEx.match(data['email']):
            flash('Email Field Invalid', 'create')
            return redirect(url_for('landing'))
        if data['first_name'] == '' or len(data['first_name']) < 2:
            flash('First Name Field Invalid', 'create')
            return redirect(url_for('landing'))
        if data['last_name'] == '' or len(data['last_name']) < 2:
            flash('Last Name Field Invalid', 'create')
            return redirect(url_for('landing'))
        if data['pass'] == '':
            flash('Password Field Invalid', 'create')
            return redirect(url_for('landing'))
        if data['pass-confirm'] != data['pass']:
            flash('Passwords do not match', 'create')
            return redirect(url_for('landing'))
        if re.match(passEx, data['pass']):
            hash = bcrypt.generate_password_hash(data['pass'])
            formData = {
                **request.form,
                'pass': hash
            }
            return formData
        else:
            flash('Password must be 8 characters long and contain one letter and one number', 'create')
            return redirect(url_for('landing'))
    
    @staticmethod
    def ValidateUserLog(data):
        if data['email'] == '':
            flash('Email field Cannot be empty', 'login')
            return redirect(url_for('landing'))
        if data['pass'] =='':
            flash('Password field cannot be empty', 'login')
            return redirect(url_for('landing'))
        return data