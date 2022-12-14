from flask_app import app
from flask import render_template, redirect, session, request, url_for
from flask_app.models.sightings_model import Sighting
from flask_app.models.user_model import User
from flask_app.models.user_model import Scrutiny


@app.route('/item/create')
def renderCreate():
    if 'id' in session:
        userData = User.getUserInfo({'id':session['id']})
        return render_template('itemform.html', userData=userData)
    else:
        return redirect(url_for('landing'))

@app.route('/item/create/validate', methods=['POST'])
def validateItemCreate():
    if 'id' in session:
        print(request.form)
        if Sighting.validateCreate(request.form):
            Sighting.create(request.form)
            return redirect(url_for('renderHome'))
        else:
            return redirect(url_for('renderCreate'))
    else:
        return redirect(url_for('landing'))

@app.route('/item/view/<int:id>')
def viewOne(id):
    if 'id' in session:
        userData = User.getUserInfo({'id':session['id']})
        sightingData = Sighting.getOneItems({'id':id})
        skepticData = Scrutiny.getSkeptics({'id':id})
        session['url'] = f'/item/view/{id}'
        return render_template('view.html', userData=userData, sightingData = sightingData, skepticData=skepticData)
    else:
        return redirect(url_for('landing'))

@app.route('/item/edit/<int:id>')
def edit(id):
    if 'id' in session:
        userData = User.getUserInfo({'id':session['id']})
        sightingData = Sighting.getOneItems({'id': id})
        return render_template('edit.html', data=sightingData, userData=userData)

@app.route('/item/edit/<int:id>/confirm', methods=['POST'])
def confirmEdit(id):
    if Sighting.validateCreate(request.form):
        data ={
            **request.form,
            'id': id
        }
        Sighting.edit(data)
        return redirect(url_for('renderHome'))
    else:
        return redirect(f"/item/edit/{id}")

@app.route('/item/delete/<int:id>')
def delete(id):
    if 'id' in session:
        Sighting.delete({'id': id})
        return redirect(url_for('renderHome'))
    else:
        return redirect(url_for('landing'))