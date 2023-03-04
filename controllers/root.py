from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connexion_db import get_db

root = Blueprint('root', __name__,
                        template_folder='templates')

@root.route('/famille/accueil/album/show')
def famille_accueil_album_show():
    mycursor = get_db().cursor()
    accreditation = session['accreditation']
    tuple_select = (accreditation)
    sql = "SELECT * FROM Albums WHERE id_accreditation_album = %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Famille/accueil.html', info_album=info_album)




