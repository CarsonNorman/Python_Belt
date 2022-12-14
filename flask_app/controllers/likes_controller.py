from flask_app import app
from flask import render_template, redirect, session, request, url_for
from flask_app.models.scrutinize_model import Scrutiny

@app.route('/like/create/<int:item>')
def createLike(item):
    if 'id' in session:
        if Scrutiny.validateLike({'user': session['id'], 'item': item}):
            Scrutiny.like({'user': session['id'], 'item': item})
            return redirect(session['url'])
        else:
            return redirect(session['url'])
    else:
        return redirect(url_for('renderHome'))
@app.route('/dislike/<int:item>')
def dislike(item):
    if 'id' in session:
        Scrutiny.dislike({'users_id':session['id'], 'items_id':item })
        return redirect(session['url'])
    else:
        return redirect(url_for('renderHome'))