from flask import Flask, request, render_template, redirect, flash, session, Blueprint
import os
import requests
import json
from werkzeug.security import generate_password_hash, check_password_hash
from connexion_db import get_db

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/admin/accueil/album/show')
def admin_accueil_album_show():
    mycursor = get_db().cursor()
    accreditation = session['accreditation']
    tuple_select = (accreditation)
    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Administrateur/accueil.html', info_album=info_album)

@admin.route('/admin/accueil/show')
def admin_accueil_show():
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
    return render_template('Administrateur/accueil.html', image_accueil=image_accueil, texte_accueil=texte_accueil, albums_accueil=albums_accueil)


@admin.route('/admin/liste/album/show')
def admin_liste_album_show():
    mycursor = get_db().cursor()
    if session['accreditation'] >= 1 or session['accreditation'] <= 4:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)
    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Administrateur/liste_album.html', info_album=info_album)


@admin.route('/admin/liste/medias/show')
def admin_accueil_medias_show():
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
    return render_template('Administrateur/liste_medias.html', info_medias=info_medias, image=image, video=video,
                           audio=audio)


@admin.route('/admin/info_user/show')
def admin_info_user_show():
    mycursor = get_db().cursor()
    if session['login']:
        tuple_select = (session['login'])
        sql = "SELECT login AS pseudo, password, prenom_utilisateur AS prenom, nom_utilisateur AS nom, mail_utilisateur AS mail FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select)
        info_user = mycursor.fetchall()
        return render_template('Administrateur/info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@admin.route('/admin/info_user/edit', methods=["GET"])
def admin_info_user_edit_get():
    mycursor = get_db().cursor()
    if session['login']:
        tuple_select = (session['login'])
        sql = "SELECT * FROM Utilisateurs WHERE login = %s;"
        mycursor.execute(sql, tuple_select)
        info_user = mycursor.fetchone()
        return render_template('Administrateur/edit_info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@admin.route('/admin/info_user/edit', methods=["POST"])
def admin_info_user_edit_post():
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
        return render_template('Administrateur/info_user.html', info_user=info_user)
    else:
        flash(u'Cette action nécessite un compte utilisateur ! Veuillez vous connecter ou bien crée un compte.',
              'alert-warning')
        return redirect('/login')


@admin.route('/admin/suppr_compte')
def admin_suppr_compte():
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


@admin.route('/admin/a_propos')
def admin_a_propos_de_nous():
    mycursor = get_db().cursor()
    sql = "SELECT titre_a_propos AS titre, texte_a_propos AS texte FROM a_propos;"
    mycursor.execute(sql)
    texte = mycursor.fetchall()
    return render_template('Administrateur/a_propos.html', texte=texte)


@admin.route('/admin/albums/show')
def admin_show_albums():
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
    return render_template('Administrateur/album.html', infos_albums=infos_albums, infos_medias=infos_medias)


@admin.route('/admin/medias/show')
def admin_show_medias():
    mycursor = get_db().cursor()
    id_medias = request.args.get('id_medias')
    tuple_select = (id_medias,)
    sql = "SELECT * FROM Medias WHERE id_medias = %s;"
    mycursor.execute(sql, tuple_select)
    infos_medias = mycursor.fetchall()
    return render_template('Administrateur/medias.html', infos_medias=infos_medias)




@admin.route('/admin/edition/show')
def admin_edition_show():
    if session['accreditation'] == 2:
        return render_template('Administrateur/edition.html')
    else:
        return render_template('Tout_le_monde/accueil.html')



"""
Edition de l'image de l'accueil
"""
@admin.route('/admin/edition/accueil/image')
def admin_edition_accueil_image():
    mycursor = get_db().cursor()
    sql = "SELECT libelle_image_accueil AS image FROM image_accueil;"
    mycursor.execute(sql)
    infos_accueil = mycursor.fetchall()
    sql = "SELECT lien_medias AS image, libelle_medias AS libelle FROM Medias WHERE id_type_medias = 1;"
    mycursor.execute(sql)
    infos_medias = mycursor.fetchall()
    return render_template('Administrateur/edition_accueil_image.html', infos_accueil=infos_accueil, infos_medias=infos_medias)


@admin.route('/admin/edition/accueil/image/update')
def admin_edition_accueil_image_update():
    mycursor = get_db().cursor()
    lien = request.args.get('lien')
    sql = "UPDATE image_accueil SET libelle_image_accueil = %s WHERE id_image_accueil = 1;"
    mycursor.execute(sql, (lien,))
    get_db().commit()
    return redirect('/admin/edition/accueil/image')



"""
Edition des albums de l'accueil
"""
@admin.route('/admin/edition/accueil/albums/show')
def admin_edition_accueil_albums_show():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Albums WHERE id_album IN (SELECT id_album_accueil FROM albums_accueil);"
    mycursor.execute(sql)
    infos_albums_actuels = mycursor.fetchall()
    sql = "SELECT * FROM Albums WHERE id_album NOT IN (SELECT id_album_accueil FROM albums_accueil);"
    mycursor.execute(sql)
    infos_albums_disponible = mycursor.fetchall()
    return render_template('Administrateur/edit_albums_accueil.html', infos_albums_actuels=infos_albums_actuels, infos_albums_disponible=infos_albums_disponible)


@admin.route('/admin/edition/accueil/albums/update')
def admin_edition_accueil_albums_update():
    mycursor = get_db().cursor()
    id_album = request.args.get('id_album')
    update = request.args.get('update')
    if update == 'delete':
        sql = "DELETE FROM albums_accueil WHERE id_album_accueil = %s;"
        mycursor.execute(sql, (id_album,))
        get_db().commit()
    if update == 'add':
        sql = "INSERT INTO albums_accueil(id_album_accueil) VALUES (%s);"
        mycursor.execute(sql, (id_album,))
        get_db().commit()
    return redirect('/admin/edition/accueil/albums/show')



"""
Edition du texte de l'acueil
"""
@admin.route('/admin/edition/accueil/texte/show')
def admin_edition_accueil_texte_show():
    mycursor = get_db().cursor()
    sql = "SELECT texte_accueil AS texte FROM texte_accueil;"
    mycursor.execute(sql)
    texte = mycursor.fetchall()
    return render_template('Administrateur/edit_texte_accueil.html', texte=texte)


@admin.route('/admin/edition/accueil/texte/update')
def admin_edition_accueil_texte_update():
    mycursor = get_db().cursor()
    texte = request.args.get('texte')
    texte_modifie = texte.replace('\n', '<br>')
    sql = "UPDATE texte_accueil SET texte_accueil = %s WHERE id_text_accueil = 1;"
    mycursor.execute(sql, (texte_modifie,))
    get_db().commit()
    return redirect('/admin/edition/show')



"""
Ajouter un albums
Affiche dans un premier temps le formulaire pour crée un albums
Ensuite affiche une page pour ajouter une image de garde et des médias
Puis ensuite valide ce formulaire et crée l'albums
"""
@admin.route('/admin/edition/albums/add/show')
def admin_edition_albums_add_show():
    return render_template('Administrateur/edition_albums_add.html')


@admin.route('/admin/edition/albums/add/text')
def admin_edition_albums_add_text():
    mycursor = get_db().cursor()
    if session['accreditation'] >= 1 or session['accreditation'] <= 4:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation,)

    #Il faut récupérer ici
    # le nom de l'album,
    nom = request.form.get('nom')
    # la description,
    description = request.form.get('description')
    # le texte de description,
    text_description = request.form.get('text_description')
    # la date de l'album,
    date = request.form.get('date')
    # si oui ou non l'uitilisateur veut mettre une image de garde est des médias
    image_garde = request.form.get('image_garde')
    medias = request.form.get('medias')
    print("Nom : " + nom)
    print("Description : " + description)
    print("Texte description : " + text_description)
    print("Date : " + date)
    print("Image de garde : " + image_garde)
    print("Médias : " + medias)


    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Administrateur/edition_albums_show.html', info_album=info_album)


@admin.route('/admin/edition/albums/add/medias')
def admin_edition_albums_add_medias():
    mycursor = get_db().cursor()
    if session['accreditation'] >= 1 or session['accreditation'] <= 4:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)

    #Il faut ici regarder les médias qui peuvent être ajouter pour les ajouter.

    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Administrateur/edition_albums_show.html', info_album=info_album)


@admin.route('/admin/edition/albums/add/garde')
def admin_edition_albums_add_garde():
    mycursor = get_db().cursor()
    if session['accreditation'] >= 1 or session['accreditation'] <= 4:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)

    #Il faut ici regarder les images de gardes qui peuvent être ajouter.

    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Administrateur/edition_albums_show.html', info_album=info_album)


@admin.route('/admin/edition/albums/add')
def admin_edition_albums_add():
    mycursor = get_db().cursor()
    if session['accreditation'] >= 1 or session['accreditation'] <= 4:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)
    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Administrateur/edition_albums_show.html', info_album=info_album)



"""
Affiche la list des albums déjà existant pour pouvoir ensuite les éditer.
"""
@admin.route('/admin/edition/albums/show')
def admin_edition_albums_show():
    mycursor = get_db().cursor()
    if session['accreditation'] >= 1 or session['accreditation'] <= 4:
        accreditation = session['accreditation']
    else:
        accreditation = 4
    tuple_select = (accreditation)
    sql = "SELECT * FROM Albums WHERE id_accreditation_album >= %s;"
    mycursor.execute(sql, tuple_select)
    info_album = mycursor.fetchall()
    return render_template('Administrateur/edition_albums_show.html', info_album=info_album)



