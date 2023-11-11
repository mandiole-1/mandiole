from flask import Flask, request, render_template, redirect, flash, session, Blueprint
import os
import requests
import json
from werkzeug.security import generate_password_hash, check_password_hash
from connexion_db import get_db

root = Blueprint('root', __name__, template_folder='templates')


@root.route('/root/accueil/album/show')
def root_accueil_album_show():
    mycursor = get_db().cursor()
    accreditation = session['accreditation']
    tuple_select = (accreditation)
    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchone()
    return render_template('Root/accueil.html', info_album=info_album)

@root.route('/root/accueil/show')
def root_accueil_show():
    mycursor = get_db().cursor()
    sql = "SELECT libelle_image_accueil FROM image_accueil;"
    mycursor.execute(sql)
    image_accueil = mycursor.fetchall()
    sql = "SELECT * FROM texte_accueil;"
    mycursor.execute(sql)
    texte_accueil = mycursor.fetchall()
    tuple_select_albums = (session['accreditation'])
    sql = "SELECT * FROM Albums INNER JOIN albums_accueil ON Albums.id_album = albums_accueil.id_album_accueil WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select_albums)
    albums_accueil = mycursor.fetchall()
    return render_template('Root/accueil.html', image_accueil=image_accueil, texte_accueil=texte_accueil, albums_accueil=albums_accueil)


@root.route('/root/liste/album/show')
def root_liste_album_show():
    mycursor = get_db().cursor()
    if session['accreditation'] >= 1 or session['accreditation'] <= 4:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)
    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Root/liste_album.html', info_album=info_album)


@root.route('/root/liste/medias/show')
def root_accueil_medias_show():
    mycursor = get_db().cursor()
    if session['accreditation']:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)
    sql = "SELECT * FROM Medias WHERE id_accreditation_medias >= %s;"
    mycursor.execute(sql, tuple_select)
    info_medias = mycursor.fetchall()
    sql1 = "SELECT id_type_medias FROM Types where id_type_medias = 1;"
    sql2 = "SELECT id_type_medias FROM Types where id_type_medias = 2;"
    sql3 = "SELECT id_type_medias FROM Types where id_type_medias = 3;"
    mycursor.execute(sql1)
    image = mycursor.fetchone()
    mycursor.execute(sql2)
    video = mycursor.fetchone()
    mycursor.execute(sql3)
    audio = mycursor.fetchone()
    return render_template('Root/liste_medias.html', info_medias=info_medias, image=image, video=video,
                           audio=audio)


@root.route('/root/info_user/show')
def root_info_user_show():
    mycursor = get_db().cursor()
    if session['login']:
        tuple_select = (session['login'])
        sql = "SELECT login AS pseudo, password, prenom_utilisateur AS prenom, nom_utilisateur AS nom, mail_utilisateur AS mail FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select)
        info_user = mycursor.fetchall()
        return render_template('Root/info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@root.route('/root/info_user/edit', methods=["GET"])
def root_info_user_edit_get():
    mycursor = get_db().cursor()
    if session['login']:
        tuple_select = (session['login'])
        sql = "SELECT * FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select)
        info_user = mycursor.fetchone()
        return render_template('Root/edit_info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@root.route('/root/info_user/edit', methods=["POST"])
def root_info_user_edit_post():
    mycursor = get_db().cursor()
    if session['login']:
        new_login = request.form.get('login')
        new_password = request.form.get('password')
        new_nom = request.form.get('nom')
        new_prenom = request.form.get('prenom')
        new_mail = request.form.get('mail')
        old_login = session['login']
        tuple_edit = (new_login, new_password, new_nom, new_prenom, new_mail, old_login)
        sql = "SELECT id_medias FROM Medias WHERE login = %s;"
        mycursor.execute(sql, (old_login,))
        medias = mycursor.fetchall()
        if len(medias) != 0 and new_login != old_login:
            flash(u'Vous ne pouvez pas modifier votre pseudo !', 'alert-warning')
            sql = "SELECT login AS pseudo, password, prenom_utilisateur AS prenom, nom_utilisateur AS nom, mail_utilisateur AS mail FROM Utilisateurs WHERE login = %s;"
            tuple_select = (session['login'])
            mycursor.execute(sql, tuple_select)
            info_user = mycursor.fetchall()
            return render_template('Root/info_user.html', info_user=info_user)
        sql = "UPDATE Utilisateurs SET login = %s, password = %s, nom_utilisateur = %s, prenom_utilisateur = %s , mail_utilisateur = %s WHERE login = %s;"
        mycursor.execute(sql, tuple_edit)
        flash(u'Modifications réussites !', 'alert-success')
        session['login'] = new_login
        tuple_select = (session['login'])
        sql = "SELECT * FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select)
        user = mycursor.fetchone()
        session['login'] = user['login']
        session['password'] = user['password']
        session['nom'] = user['nom_utilisateur']
        session['prenom'] = user['prenom_utilisateur']
        session['mail'] = user['mail_utilisateur']
        session['accreditation'] = user['id_accreditation_utilisateur']
        tuple_select = (session['login'])
        sql = "SELECT login AS pseudo, password, prenom_utilisateur AS prenom, nom_utilisateur AS nom, mail_utilisateur AS mail FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select)
        info_user = mycursor.fetchall()
        return render_template('Root/info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@root.route('/root/suppr_compte')
def root_suppr_compte():
    mycursor = get_db().cursor()
    recipient_email = session['mail']
    login = session['login']
    password = session['password']
    nom = session['nom']
    prenom = session['prenom']
    sql = "SELECT libelle_key FROM api_key_sendinblue;"
    mycursor.execute(sql)
    api_key = mycursor.fetchone()
    url = "https://api.sendinblue.com/v3/smtp/email"
    payload = {
        "sender": {"name": "Mandiole", "email": "mandiole.services@gmail.com"},
        "to": [{"email": recipient_email}],
        "subject": "Compte supprimé",
        "htmlContent": "<html><body><p>Bonjour " + prenom + " " + nom + ", suite à votre demande en ligne votre compte à été supprimer.</p></body></html>"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(response.json())
    sql = "DELETE FROM Utilisateurs WHERE login = %s;"
    mycursor.execute(sql, (login))
    get_db().commit()
    flash(u'Votre compte à été supprimer !', 'alert-warning')
    return redirect('/')


@root.route('/root/a_propos')
def root_a_propos_de_nous():
    mycursor = get_db().cursor()
    sql = "SELECT titre_a_propos AS titre, texte_a_propos AS texte FROM a_propos;"
    mycursor.execute(sql)
    texte = mycursor.fetchall()
    return render_template('Root/a_propos.html', texte=texte)


@root.route('/root/albums/show')
def root_show_albums():
    mycursor = get_db().cursor()
    id_album = request.args.get('id_album')
    id_accreditation = session['accreditation']
    tuple_select = (id_album, id_accreditation)
    sql = "SELECT * FROM Albums WHERE id_album = %s AND id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    infos_albums = mycursor.fetchall()
    tuple_select = (id_album, id_accreditation)
    sql = "SELECT * FROM Medias INNER JOIN medias_album ma on Medias.id_medias = ma.id_medias WHERE id_album = %s AND Medias.id_medias = ma.id_medias AND id_accreditation_medias >= %s;"
    mycursor.execute(sql, tuple_select)
    infos_medias = mycursor.fetchall()
    return render_template('Root/album.html', infos_albums=infos_albums, infos_medias=infos_medias)


@root.route('/root/medias/show')
def root_show_medias():
    mycursor = get_db().cursor()
    id_medias = request.args.get('id_medias')
    tuple_select = (id_medias,)
    sql = "SELECT * FROM Medias WHERE id_medias = %s;"
    mycursor.execute(sql, tuple_select)
    infos_medias = mycursor.fetchall()
    return render_template('Root/medias.html', infos_medias=infos_medias)


@root.route('/root/perso')
def root_show_perso():
    if session['accreditation'] == 1:
        return render_template('Root/Perso/perso.html')
    else:
        return redirect('/autres/accueil/show')