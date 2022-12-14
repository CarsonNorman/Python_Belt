from flask_app import app, bcrypt
from flask import render_template as render, redirect, request, session, flash, url_for
from flask_app.models.login_model import Login
from flask_app.models.user_model import User
from flask_app.models.sightings_model import Sighting


@app.route('/')
def landing():
    return render('landing.html')

@app.route('/validateCreate', methods=['POST'])
def validateUserCreate():
        return Login.create(Login.ValidateUserCreate(request.form))
    

@app.route('/validateLog', methods=['POST'])
def validateLog():  
    return Login.login(Login.ValidateUserLog(request.form))

@app.route('/logout')
def logout():
    Login.logout()
    return redirect(url_for('landing'))

@app.route('/dashboard')
def renderHome():
    if 'id' in session:
        # userData = User.get_one({'id':session['id']})
        userData = User.getUserInfo({'id':session['id']})
        itemsData = Sighting.getAllItems()
        session['url'] = '/dashboard'
        return render('dashboard.html', userData = userData, itemsData = itemsData)
    else: 
        flash('Please Login', 'login')
        return redirect(url_for('landing'))