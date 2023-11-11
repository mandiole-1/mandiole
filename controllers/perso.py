from flask import Flask, request, render_template, redirect, flash, session, Blueprint
import os
import requests
import json
from werkzeug.security import generate_password_hash, check_password_hash
from connexion_db import get_db

import instaloader
import os
import time
import subprocess
import sys
import shutil
import json

perso = Blueprint('perso', __name__, template_folder='templates')


@perso.route('/perso/instagram/show')
def perso_instagram_show():
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        sql = "SELECT id_user, nom_utilisateur, libelle_medias FROM user_instagram JOIN medias_instagram mi on user_instagram.id_user = mi.user_id WHERE photo_profile = 1 ORDER BY nom_utilisateur;"
        mycursor.execute(sql)
        infos_user_photo = mycursor.fetchall()

        sql = "SELECT id_user, nom_utilisateur FROM user_instagram WHERE id_user NOT IN (SELECT id_user FROM user_instagram JOIN medias_instagram mi on user_instagram.id_user = mi.user_id WHERE photo_profile = 1 ORDER BY nom_utilisateur) ORDER BY nom_utilisateur;"
        mycursor.execute(sql)
        infos_user_no_photo = mycursor.fetchall()
        return render_template('Root/Perso/instagram.html', infos_user_photo=infos_user_photo,
                               infos_user_no_photo=infos_user_no_photo)
    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/update_one')
def perso_instagram_update_one():
    if session['accreditation'] == 1:
        id_user = request.args.get("id_user", "")
        perso_instagram_update_post(id_user)
        perso_instagram_update_profile(id_user)
        return redirect('/perso/instagram/show')
    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/get_nb_compte')
def perso_instagram_get_nb_compte():
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        sql = "SELECT id_user FROM user_instagram ORDER BY nom_utilisateur;"
        mycursor.execute(sql)
        rows = mycursor.fetchall()
        nb = [row['id_user'] for row in rows]
        json_data = json.dumps(nb)
        return json_data
    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/update_all')
def perso_instagram_update_all():
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        sql = "SELECT id_user AS id FROM user_instagram ORDER BY nom_utilisateur;"
        mycursor.execute(sql)
        list_user = mycursor.fetchall()
        for user in list_user:
            perso_instagram_update_post(user['id'])
            perso_instagram_update_profile(user['id'])
        return redirect('/perso/instagram/show')
    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/update/profile')
def perso_instagram_update_profile(id_user):
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        sql = "SELECT nom_utilisateur FROM user_instagram WHERE id_user = %s;"
        mycursor.execute(sql, (id_user,))
        nom_utilisateur = mycursor.fetchone()

        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, nom_utilisateur['nom_utilisateur'])
        L.download_profilepic(profile)

        dossier = nom_utilisateur['nom_utilisateur']
        photo_profile = []
        if os.path.exists(dossier) and os.path.isdir(dossier):
            for nom_fichier in os.listdir(dossier):
                chemin_fichier = os.path.join(dossier, nom_fichier)
                if os.path.isfile(chemin_fichier):
                    photo_profile.append(chemin_fichier)

        nom_photo = photo_profile[0].split("/")

        chemin_origine = "/home/arthur/Documents/Perso/Mandiole/" + photo_profile[0]
        chemin_destination = "/home/arthur/Documents/Perso/Mandiole/static/Perso"
        chemin_dossier = "/home/arthur/Documents/Perso/Mandiole/" + nom_utilisateur['nom_utilisateur']

        sql = "SELECT COUNT(id_medias) AS nb FROM medias_instagram WHERE libelle_medias = %s;"
        mycursor.execute(sql, (nom_photo[1]))
        photo = mycursor.fetchone()

        if photo['nb'] == 0:
            tuple_insert = (id_user, nom_photo[1], 1)
            sql = "INSERT INTO medias_instagram(id_medias, user_id, libelle_medias, photo_profile) VALUES (NULL, %s, %s, %s);"
            mycursor.execute(sql, tuple_insert)
            get_db().commit()
            shutil.move(chemin_origine, chemin_destination)
            shutil.rmtree(chemin_dossier)
        else:
            shutil.rmtree(chemin_dossier)

    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/update/post')
def perso_instagram_update_post(id_user):
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        sql = "SELECT nom_utilisateur FROM user_instagram WHERE id_user = %s;"
        mycursor.execute(sql, (id_user,))
        nom_utilisateur = mycursor.fetchone()

        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, nom_utilisateur['nom_utilisateur'])
        for post in profile.get_posts():
            L.download_post(post, target=nom_utilisateur['nom_utilisateur'])

        dossier = nom_utilisateur['nom_utilisateur']
        list_post = []
        if os.path.exists(dossier) and os.path.isdir(dossier):
            for nom_fichier in os.listdir(dossier):
                chemin_fichier = os.path.join(dossier, nom_fichier)
                if os.path.isfile(chemin_fichier):
                    list_post.append(chemin_fichier)

        for post in list_post:
            nom_photo = post.split("/")

            chemin_origine = "/home/arthur/Documents/Perso/Mandiole/" + post
            chemin_destination = "/home/arthur/Documents/Perso/Mandiole/static/Perso"
            chemin_dossier = "/home/arthur/Documents/Perso/Mandiole/" + nom_utilisateur['nom_utilisateur']

            sql = "SELECT COUNT(id_medias) AS nb FROM medias_instagram WHERE libelle_medias = %s;"
            mycursor.execute(sql, (nom_photo[1]))
            photo = mycursor.fetchone()

            if photo['nb'] == 0:
                tuple_insert = (id_user, nom_photo[1], 0)
                sql = "INSERT INTO medias_instagram(id_medias, user_id, libelle_medias, photo_profile) VALUES (NULL, %s, %s, %s);"
                mycursor.execute(sql, tuple_insert)
                get_db().commit()
                shutil.move(chemin_origine, chemin_destination)

        chemin_dossier = "/home/arthur/Documents/Perso/Mandiole/" + nom_utilisateur['nom_utilisateur']
        if os.path.exists(dossier) and os.path.isdir(dossier):
            shutil.rmtree(chemin_dossier)

    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/show/user')
def perso_instagram_show_user():
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        id_user = request.args.get("id_user", "")
        sql = "SELECT (SELECT libelle_medias FROM user_instagram JOIN medias_instagram mi on user_instagram.id_user = mi.user_id WHERE photo_profile = 1 AND id_user = %s) AS photo_profile, nom_utilisateur, id_user FROM user_instagram JOIN medias_instagram mi on user_instagram.id_user = mi.user_id WHERE id_user = %s GROUP BY id_user;"
        mycursor.execute(sql, (id_user, id_user))
        infos_user = mycursor.fetchall()
        sql = "SELECT libelle_medias AS lien_medias, id_medias FROM medias_instagram JOIN user_instagram ui on ui.id_user = medias_instagram.user_id WHERE id_user = %s;"
        mycursor.execute(sql, (id_user,))
        infos_medias = mycursor.fetchall()
        return render_template('Root/Perso/infos_user.html', infos_user=infos_user, infos_medias=infos_medias)
    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/delete')
def perso_instagram_delete():
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        id_user = request.args.get("id_user")
        sql = "DELETE FROM medias_instagram WHERE user_id = %s;"
        mycursor.execute(sql, (id_user,))
        get_db().commit()
        sql = "DELETE FROM user_instagram WHERE id_user = %s;"
        mycursor.execute(sql, (id_user,))
        get_db().commit()
        return redirect('/perso/instagram/show')
    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/show/medias')
def perso_instagram_show_medias():
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        id_medias = request.args.get("id_medias", "")
        sql = "SELECT libelle_medias AS lien_medias, id_medias FROM medias_instagram WHERE id_medias = %s;"
        mycursor.execute(sql, (id_medias,))
        infos_medias = mycursor.fetchall()
        return render_template('Root/Perso/infos_medias.html', infos_medias=infos_medias)
    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/user/add')
def perso_instagram_user_add():
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        nom_utilisateur = request.args.get('nom_utilisateur')
        sql = "INSERT INTO user_instagram(id_user, nom_utilisateur) VALUES (NULL, %s);"
        mycursor.execute(sql, (nom_utilisateur,))
        get_db().commit()
        return redirect('/perso/instagram/show')
    else:
        return redirect('/autres/accueil/show')


@perso.route('/perso/instagram/medias/show/all')
def perso_instagram_medias_show_all():
    if session['accreditation'] == 1:
        mycursor = get_db().cursor()
        sql = "SELECT id_medias, libelle_medias AS lien_medias FROM medias_instagram ORDER BY id_medias;"
        mycursor.execute(sql)
        infos_medias = mycursor.fetchall()
        return render_template('Root/Perso/all_medias.html', infos_medias=infos_medias)
    else:
        return redirect('/autres/accueil/show')