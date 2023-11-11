from flask import Flask, request, render_template, redirect, flash, session, Blueprint
# import os
import requests
import json
# from werkzeug.security import generate_password_hash, check_password_hash
from connexion_db import get_db

autre_connection = Blueprint('autre_connection', __name__, template_folder='templates')


@autre_connection.route('/login')
def autre_login():
    return render_template('Tout_le_monde/connection_compte.html')


@autre_connection.route('/login', methods=["POST"])
def autre_login_post():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    password = request.form.get('password')
    tuple_select = (login, password)
    sql = "SELECT * FROM Utilisateurs WHERE login = %s AND password = %s;"
    mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    if user:
        session['login'] = user['login']
        session['password'] = user['password']
        session['nom'] = user['nom_utilisateur']
        session['prenom'] = user['prenom_utilisateur']
        session['accreditation'] = user['id_accreditation_utilisateur']
        session['mail'] = user['mail_utilisateur']
        if session['accreditation'] == 1:
            flash(u'Connexion réussite ! Vous êtes connecter entant que Root.', 'alert-success')
            return redirect('/root/accueil/show')
        elif session['accreditation'] == 2:
            flash(u'Connexion réussite ! Vous êtes connecter entant que Administrateur.', 'alert-success')
            return redirect('/admin/accueil/show')
        elif session['accreditation'] == 3:
            flash(u'Connexion réussite ! Vous êtes connecter entant que Famille.', 'alert-success')
            return redirect('/famille/accueil/show')
        else:
            flash(u'Connexion réussite !', 'alert-success')
            return redirect('/autres/accueil/show')
    else:
        flash(u'Login ou mots de passe incorrect !', 'alert-warning')
        return redirect('/login')


@autre_connection.route('/signup')
def auth_signup():
    return render_template('Tout_le_monde/creer_compte.html')


@autre_connection.route('/signup', methods=["POST"])
def auth_signup_post():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    password = request.form.get('password')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    mail = request.form.get('email')
    sql = "SELECT libelle_key FROM api_key_sendinblue;"
    mycursor.execute(sql)
    api_key = mycursor.fetchone()
    tuple_select = (login, mail)
    sql = "SELECT * FROM Utilisateurs WHERE login = %s OR mail_utilisateur = %s;"
    mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    if user:
        flash(u'Votre adresse Email ou votre login existe déjà !', 'alert-warning')
        return redirect('/signup')
    # password = generate_password_hash(password, method='sha256')
    tuple_insert = (login, password, nom, prenom, mail, 4)
    sql = "INSERT INTO Utilisateurs (login, password, nom_utilisateur, prenom_utilisateur, mail_utilisateur, id_accreditation_utilisateur) VALUES (%s, %s, %s, %s, %s, %s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    url = "https://api.sendinblue.com/v3/smtp/email"
    payload = {
        "sender": {"name": "Mandiole", "email": "mandiole.services@gmail.com"},
        "to": [{"email": mail}],
        "subject": "Création du compte",
        "htmlContent": "<html><body><p>Bonjour " + prenom + " " + nom + ", suite à votre demande en ligne de création de compte, voici vos identifiants de connections : <br> Login : " + login + "<br>Mots de passe : " + password + "</p></body></html>"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        flash(u'Compte utilisateur trouver, un mail vas vous être envoyer !', 'alert-success')
        return redirect('/login')
    else:
        flash(u'Compte utilisateur trouver, mail non envoyer ! Veuillez nous contacter si le problème persiste.',
              'alert-warning')
        return render_template('Tout_le_monde/mots_de_passe_oublie.html')


@autre_connection.route('/logout')
def auth_logout():
    session['login'] = None
    session['password'] = None
    session['nom'] = None
    session['prenom'] = None
    session['accreditation'] = 4
    flash(u'Déconnexion réussi !', 'alert-success')
    return redirect('/autres/accueil/show')


@autre_connection.route('/forget-password', methods=["GET"])
def forget_password():
    return render_template('Tout_le_monde/mots_de_passe_oublie.html')


@autre_connection.route('/forget-password', methods=["POST"])
def forget_password_envoi():
    login = request.form.get('login')
    email = request.form.get('mail')
    mycursor = get_db().cursor()
    tuple_select_login = login
    tuple_select_mail = email
    tuple_select = (login, email)
    sql = "SELECT libelle_key FROM api_key_sendinblue;"
    mycursor.execute(sql)
    api_key = mycursor.fetchone()
    if login == None and email != None:
        sql = "SELECT COUNT(login) AS nb FROM Utilisateurs WHERE mail_utilisateur = %s;"
        mycursor.execute(sql, tuple_select_mail)
    elif login != None and email == None:
        sql = "SELECT COUNT(login) AS nb FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select_login)
    elif login != None and email != None:
        sql = "SELECT COUNT(login) AS nb FROM Utilisateurs WHERE login = %s OR mail_utilisateur = %s;"
        mycursor.execute(sql, tuple_select)
    nb_utilisateur = mycursor.fetchone()
    if nb_utilisateur['nb'] == 0:
        flash(u'Aucun compte utilisateur ne possède ce pseudo ou cette adresse mail !', 'alert-warning')
        return render_template('Tout_le_monde/mots_de_passe_oublie.html')
    elif nb_utilisateur['nb'] == 1:
        if login == None and email != None:
            sql = "SELECT * FROM Utilisateurs WHERE mail_utilisateur = %s;"
            mycursor.execute(sql, tuple_select_mail)
        elif login != None and email == None:
            sql = "SELECT * FROM Utilisateurs WHERE login = %s;"
            mycursor.execute(sql, tuple_select_login)
        elif login != None and email != None:
            sql = "SELECT * FROM Utilisateurs WHERE login = %s OR mail_utilisateur = %s;"
            mycursor.execute(sql, tuple_select)
        infos_utilisateur = mycursor.fetchone()
        recipient_email = infos_utilisateur['mail_utilisateur']
        login = infos_utilisateur['login']
        password = infos_utilisateur['password']
        nom = infos_utilisateur['nom_utilisateur']
        prenom = infos_utilisateur['prenom_utilisateur']
        url = "https://api.sendinblue.com/v3/smtp/email"
        payload = {
            "sender": {"name": "Mandiole", "email": "mandiole.services@gmail.com"},
            "to": [{"email": recipient_email}],
            "subject": "Mot de passe oublié",
            "htmlContent": "<html><body><p>Bonjour " + prenom + " " + nom + ", suite à votre demande en ligne voici vos identifiants de connections : <br> Login : " + login + "<br>Mots de passe : " + password + "</p></body></html>"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": api_key
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 201:
            flash(u'Compte utilisateur trouver, un mail vas vous être envoyer !', 'alert-success')
            return redirect('/autres/accueil/show')
        else:
            flash(u'Compte utilisateur trouver, mail non envoyer ! Veuillez nous contacter si le problème persiste.',
                  'alert-warning')
            return render_template('Tout_le_monde/mots_de_passe_oublie.html')
    else:
        flash(
            u'Plusieurs utilisateurs possède le même pseudo ou le même mail que vous. Veuillez nous contacter si le problème persiste.',
            'alert-warning')
        return render_template('Tout_le_monde/mots_de_passe_oublie.html')


@autre_connection.route('/autres/accueil/show')
def autres_accueil_show():
    mycursor = get_db().cursor()
    sql = "SELECT libelle_image_accueil FROM image_accueil;"
    mycursor.execute(sql)
    image_accueil = mycursor.fetchone()
    sql = "SELECT * FROM texte_accueil;"
    mycursor.execute(sql)
    texte_accueil = mycursor.fetchall()
    tuple_select_albums = (session['accreditation'])
    sql = "SELECT * FROM Albums INNER JOIN albums_accueil ON Albums.id_album = albums_accueil.id_album_accueil WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select_albums)
    albums_accueil = mycursor.fetchall()
    return render_template('Tout_le_monde/accueil.html', image_accueil=image_accueil, texte_accueil=texte_accueil,
                           albums_accueil=albums_accueil)


@autre_connection.route('/autres/liste/album/show')
def autres_liste_album_show():
    mycursor = get_db().cursor()
    if session['accreditation'] >= 1 or session['accreditation'] <= 4:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)
    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Tout_le_monde/liste_album.html', info_album=info_album)


@autre_connection.route('/autres/liste/medias/show')
def autres_accueil_medias_show():
    mycursor = get_db().cursor()
    if session['accreditation']:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)
    sql = "SELECT * FROM Medias WHERE id_accreditation_medias = %s;"
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
    return render_template('Tout_le_monde/liste_medias.html', info_medias=info_medias, image=image, video=video,
                           audio=audio)


@autre_connection.route('/autres/info_user/show')
def autres_info_user_show():
    mycursor = get_db().cursor()
    if session['login']:
        tuple_select = (session['login'])
        sql = "SELECT login AS pseudo, password, prenom_utilisateur AS prenom, nom_utilisateur AS nom, mail_utilisateur AS mail FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select)
        info_user = mycursor.fetchall()
        return render_template('Tout_le_monde/info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@autre_connection.route('/autres/info_user/edit', methods=["GET"])
def autres_info_user_edit_get():
    mycursor = get_db().cursor()
    if session['login']:
        tuple_select = (session['login'])
        sql = "SELECT * FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select)
        info_user = mycursor.fetchone()
        return render_template('Tout_le_monde/edit_info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@autre_connection.route('/autres/info_user/edit', methods=["POST"])
def autres_info_user_edit_post():
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
        return render_template('Tout_le_monde/info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@autre_connection.route('/autres/suppr_compte')
def autres_suppr_compte():
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
    sql = "DELETE FROM Utilisateurs WHERE login = %s;"
    mycursor.execute(sql, (login))
    get_db().commit()
    flash(u'Votre compte à été supprimer !', 'alert-warning')
    return redirect('/')


@autre_connection.route('/autres/a_propos')
def autres_a_propos_de_nous():
    mycursor = get_db().cursor()
    sql = "SELECT titre_a_propos AS titre, texte_a_propos AS texte FROM a_propos;"
    mycursor.execute(sql)
    texte = mycursor.fetchall()
    return render_template('Tout_le_monde/a_propos.html', texte=texte)


@autre_connection.route('/autres/albums/show')
def autres_show_albums():
    mycursor = get_db().cursor()
    id_album = request.args.get('id_album')
    id_accreditation = session['accreditation']
    tuple_select = (id_album, id_accreditation)
    sql = "SELECT * FROM Albums WHERE id_album = %s AND id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    infos_albums = mycursor.fetchall()
    tuple_select = (id_album, id_accreditation)
    sql = "SELECT * FROM Medias INNER JOIN medias_album ma on Medias.id_medias = ma.id_medias WHERE id_album = %s AND Medias.id_medias = ma.id_medias AND id_accreditation_medias = %s;"
    mycursor.execute(sql, tuple_select)
    infos_medias = mycursor.fetchall()
    return render_template('Tout_le_monde/album.html', infos_albums=infos_albums, infos_medias=infos_medias)


@autre_connection.route('/autres/medias/show')
def autres_show_medias():
    mycursor = get_db().cursor()
    id_medias = request.args.get('id_medias')
    tuple_select = (id_medias,)
    sql = "SELECT * FROM Medias WHERE id_medias = %s;"
    mycursor.execute(sql, tuple_select)
    infos_medias = mycursor.fetchall()
    return render_template('Tout_le_monde/medias.html', infos_medias=infos_medias)