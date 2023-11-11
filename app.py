import pymysql
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint

from controllers.autre_connection import *
from controllers.famille import *
from controllers.admin import *
from controllers.root import *
from controllers.perso import *
from connexion_db import get_db


app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'



def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="akeusch",
            password="0901",
            database="Mandiole",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    mycursor = get_db().cursor()
    session['login'] = None
    session['password'] = None
    session['nom'] = None
    session['prenom'] = None
    session['accreditation'] = 4
    sql = "SELECT libelle_image_accueil FROM image_accueil;"
    mycursor.execute(sql)
    image_accueil = mycursor.fetchone()
    sql = "SELECT * FROM texte_accueil;"
    mycursor.execute(sql)
    texte_accueil = mycursor.fetchall()
    tuple_select_albums = (session['accreditation'])
    sql = "SELECT * FROM Albums INNER JOIN albums_accueil ON Albums.id_album = albums_accueil.id_album_accueil WHERE id_accreditation_album = %s;"
    mycursor.execute(sql, tuple_select_albums)
    albums_accueil = mycursor.fetchall()
    return render_template('Tout_le_monde/accueil.html', image_accueil=image_accueil, texte_accueil=texte_accueil, albums_accueil=albums_accueil)





app.register_blueprint(autre_connection)
app.register_blueprint(famille)
app.register_blueprint(admin)
app.register_blueprint(root)
app.register_blueprint(perso)




if __name__=='__main__':
    app.run()