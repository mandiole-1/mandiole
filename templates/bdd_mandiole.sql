#mysql --user=akeusch --password=0901 --host=localhost --database=Mandiole
DROP TABLE IF EXISTS medias_instagram,user_instagram,a_propos,api_key_sendinblue,albums_accueil,texte_accueil,image_accueil,medias_album, aime, Commentaire, Albums, Medias, Types, Utilisateurs, Acreditation;

CREATE TABLE IF NOT EXISTS Acreditation(
    id_accreditation INT,
    libelle_accreditation VARCHAR(200),
    PRIMARY KEY(id_accreditation)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS Utilisateurs(
    login VARCHAR(200),
    password VARCHAR(200),
    nom_utilisateur TEXT,
    prenom_utilisateur TEXT,
    mail_utilisateur TEXT,
    id_accreditation_utilisateur INT,
    PRIMARY KEY(login),
    FOREIGN KEY(id_accreditation_utilisateur) REFERENCES Acreditation(id_accreditation)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS Types(
    id_type_medias INT,
    libelle_type_medias VARCHAR(50),
    PRIMARY KEY(id_type_medias)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS Medias(
    id_medias INT AUTO_INCREMENT,
    libelle_medias TEXT,
    description_medias TEXT,
    lien_medias TEXT,
    id_type_medias INT,
    date_medias DATE,
    login VARCHAR(200),
    id_accreditation_medias INT,
    PRIMARY KEY(id_medias),
    FOREIGN KEY(id_type_medias) REFERENCES Types(id_type_medias),
    FOREIGN KEY(login) REFERENCES Utilisateurs(login),
    FOREIGN KEY(id_accreditation_medias) REFERENCES Acreditation(id_accreditation)
)CHARACTER SET 'utf8' ;

CREATE INDEX medias_libelle_medias_index ON Medias(libelle_medias);

CREATE TABLE IF NOT EXISTS Albums(
    id_album INT AUTO_INCREMENT,
    libelle_image_garde TEXT,
    libelle_album TEXT,
    description_album TEXT,
    date_album DATE,
    texte_article TEXT,
    id_accreditation_album INT,
    PRIMARY KEY(id_album),
    FOREIGN KEY(id_accreditation_album) REFERENCES Acreditation(id_accreditation)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS Commentaire(
    id_commentaire INT AUTO_INCREMENT,
    contenu_commentaire TEXT,
    login_utilisateur_commentaire VARCHAR(200),
    id_medias INT NOT NULL,
    id_autorisation_lecture INT,
    PRIMARY KEY(id_commentaire),
    FOREIGN KEY(login_utilisateur_commentaire) REFERENCES Utilisateurs(login),
    FOREIGN KEY(id_medias) REFERENCES Medias(id_medias),
    FOREIGN KEY(id_autorisation_lecture) REFERENCES Acreditation(id_accreditation)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS aime(
    login_utilisateur_aime VARCHAR(200),
    id_medias_aime INT,
    PRIMARY KEY(login_utilisateur_aime, id_medias_aime),
    FOREIGN KEY(login_utilisateur_aime) REFERENCES Utilisateurs(login),
    FOREIGN KEY(id_medias_aime) REFERENCES Medias(id_medias)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS medias_album(
    id_medias INT,
    id_album INT,
    PRIMARY KEY (id_medias, id_album),
    FOREIGN KEY(id_medias) REFERENCES Medias(id_medias),
    FOREIGN KEY(id_album) REFERENCES Albums(id_album)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS image_accueil(
    id_image_accueil INT AUTO_INCREMENT,
    libelle_image_accueil TEXT,
    PRIMARY KEY (id_image_accueil)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS texte_accueil(
    id_text_accueil INT AUTO_INCREMENT,
    texte_accueil TEXT,
    PRIMARY KEY (id_text_accueil)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS albums_accueil(
    id_album_accueil INT,
    PRIMARY KEY (id_album_accueil),
    FOREIGN KEY(id_album_accueil) REFERENCES Albums(id_album)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS api_key_sendinblue(
    id_key INT AUTO_INCREMENT,
    libelle_key TEXT,
    PRIMARY KEY (id_key)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS a_propos(
    id_texte INT AUTO_INCREMENT,
    titre_a_propos TEXT,
    texte_a_propos TEXT,
    PRIMARY KEY (id_texte)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS user_instagram(
    id_user INT AUTO_INCREMENT,
    nom_utilisateur TEXT,
    favorie INT,
    PRIMARY KEY (id_user)
)CHARACTER SET 'utf8' ;

CREATE TABLE IF NOT EXISTS medias_instagram(
    id_medias INT AUTO_INCREMENT,
    user_id INT,
    libelle_medias TEXT,
    photo_profile INT,
    PRIMARY KEY (id_medias, user_id),
    FOREIGN KEY (user_id) REFERENCES user_instagram(id_user)
)CHARACTER SET 'utf8' ;





INSERT INTO Acreditation(id_accreditation, libelle_accreditation) VALUES
    (1, 'Root'),
    (2, 'Admin'),
    (3, 'Famille'),
    (4, 'Autres');

INSERT INTO Utilisateurs(login, password, nom_utilisateur, prenom_utilisateur, mail_utilisateur, id_accreditation_utilisateur) VALUES
    ('akeusch', 'wq6xaftg', 'KEUSCH', 'Arthur', 'arthur-keusch@orange.fr', 1),
    ('admin', 'admin', 'admin', 'admin', 'arthur-keusch@orange.fr', 2),
    ('famille', 'famille', 'famille', 'famille', 'arthur-keusch@orange.fr', 3),
    ('autre', 'autre', 'autre', 'autre', 'arthur-keusch@orange.fr', 4);

INSERT INTO Types(id_type_medias, libelle_type_medias) VALUES
    (1, 'Image'),
    (2, 'Vidéo'),
    (3, 'Audio');

INSERT INTO Medias(id_medias, libelle_medias, description_medias, lien_medias, id_type_medias, date_medias, login, id_accreditation_medias) VALUES
    (NULL, 'libelle image', 'description image', 'image.jpeg', 1, '2023-02-07', 'akeusch', 4),
    (NULL, 'libelle image2', 'description image2', 'image2.jpg', 1, '2023-02-07', 'akeusch', 4),
    (NULL, 'libelle vidéo', 'description vidéo', 'video.mp4', 2, '2023-02-07', 'akeusch', 4),
    (NULL, 'libelle audio', 'description audio', 'audio.mp3', 3, '2023-02-07', 'akeusch', 4);

INSERT INTO Albums(id_album, libelle_image_garde, libelle_album, description_album, date_album, texte_article, id_accreditation_album) VALUES
    (NULL, 'image.jpeg', 'Album 1', 'Description album 1', '2023-02-07', 'Texte de description', 4),
    (NULL, 'image.jpeg', 'Album 2', 'Description album 2', '2023-02-07', 'Texte de description', 4),
    (NULL, 'image.jpeg', 'Album 3', 'Description album 3', '2023-02-07', 'Texte de description', 4),
    (NULL, 'image.jpeg', 'Album 4', 'Description album 4', '2023-02-07', 'Texte de description', 4),
    (NULL, 'image.jpeg', 'Album 5', 'Description album 5', '2023-02-07', 'Texte de description', 4);

INSERT INTO medias_album(id_medias, id_album) VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (2, 2),
    (2, 3);

INSERT INTO image_accueil(id_image_accueil, libelle_image_accueil) VALUES
    (NULL, 'image.jpeg');

INSERT INTO texte_accueil(id_text_accueil, texte_accueil) VALUES
    (NULL, 'Je test la mise en page du texte.<br>Il faudras plus tard compléter cette partie de la base de donnée pour avoir un cour texte de présnetation du site internet. Mais en attendant je avis mettre quelques lignes pour simuler un long texte sur le sujet. Mais comme je ne sais pas quoi dire je vais mettre plein de choses inutiles.');

INSERT INTO albums_accueil(id_album_accueil) VALUES
    (1),
    (2),
    (3),
    (4);

INSERT INTO api_key_sendinblue(id_key, libelle_key) VALUES
    (NULL, 'clé_api_sendiblue_a_renseigner');

INSERT INTO a_propos(id_texte, titre_a_propos, texte_a_propos) VALUES
    (NULL, 'Titre 1', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ornare ante ut dolor consequat elementum.
    Praesent mi arcu, varius a metus id, commodo rhoncus nulla. Praesent quis eleifend justo. Quisque tellus felis, tincidunt ac varius a,
    ornare eu metus. Integer lacinia erat congue dolor fermentum, nec rutrum ante congue. Orci varius natoque penatibus et magnis dis parturient montes,
    nascetur ridiculus mus. Quisque lobortis est eros. Cras lorem ligula, efficitur sit amet feugiat nec, dignissim non risus. Ut eu rhoncus metus.
    Sed vitae molestie arcu. Maecenas varius mauris sed mauris varius sodales.'),
    (NULL, 'Titre 2', 'Suspendisse fermentum massa id vehicula pretium. Fusce egestas magna tellus, at hendrerit dolor posuere ac. Nullam molestie euismod erat nec
    volutpat. Nunc consequat ut lectus a hendrerit. Sed lorem odio, laoreet ut ex eget, tempor suscipit tortor. Sed congue tellus vitae velit venenatis,
    quis finibus arcu elementum. Cras vulputate lorem vitae ex cursus, ut pretium magna hendrerit. Phasellus nec lacinia massa. Mauris elementum est eu
    feugiat suscipit. Vivamus dignissim tellus vel libero faucibus, sed venenatis sem posuere. Duis et tempus turpis.'),
    (NULL, 'Titre 3', 'Proin ac egestas est. Sed viverra magna id justo fermentum lacinia. Vestibulum id enim dictum, fringilla sapien nec, facilisis felis. Quisque
    iaculis ullamcorper massa, vitae ullamcorper magna porta id. Nam a libero justo. Aenean efficitur non sem a placerat. Duis egestas et mauris ut
    varius. Mauris ut varius risus. Cras tempor molestie augue a euismod. Aliquam vel arcu efficitur, pharetra magna id, tincidunt massa. Etiam sed
    fringilla nibh. In hac habitasse platea dictumst. Donec dui enim, ultricies nec volutpat eu, tempus eget quam. Donec mattis, quam at rutrum pretium,
    justo turpis sollicitudin tortor, auctor efficitur ligula erat non tellus.');

INSERT INTO user_instagram(id_user, nom_utilisateur) VALUES
    (NULL, 'g_kln1'),
    (NULL, 'cecile_kuz'),
    (NULL, '_.c.l.a.r.0._'),
    (NULL, 'eddy.morisot'),
    (NULL, 'lilyycrxx'),
    (NULL, '___martine____'),
    (NULL, 'jacqueselodie_'),
    (NULL, '_juliettepnd_'),
    (NULL, 'tom_patton_70'),
    (NULL, 'louise_vn_'),
    (NULL, 'cger_ard'),
    (NULL, 'eline.jnt'),
    (NULL, 'm_non_a'),
    (NULL, '_zoevx'),
    (NULL, 'clem_rmr'),
    (NULL, 'lou_louuprv'),
    (NULL, 'regnaudsacha'),
    (NULL, 'alicia.rdy'),
    (NULL, 'elisa_cousin'),
    (NULL, 'zoe.ctl'),
    (NULL, 'louisehumbert_'),
    (NULL, 'yael_sllrd'),
    (NULL, 'emmaaa_prt'),
    (NULL, 'alixia_blz'),
    (NULL, 'g_kln2'),
    (NULL, 'l_slk10'),
    (NULL, 'chloeprt04'),
    (NULL, 'maenafrancois595'),
    (NULL, 'qtrn_valentine'),
    (NULL, 'eva.prt_'),
    (NULL, 'eli.cslo'),
    (NULL, 'florine_j17'),
    (NULL, 'lea__just__lea'),
    (NULL, 'holyvirgincarla'),
    (NULL, 'lea.ferry25'),
    (NULL, 'eli__s4'),
    (NULL, 'oceane_kost'),
    (NULL, 'jeaanne_mlt'),
    (NULL, 'math_658'),
    (NULL, 'emelyne_gcv'),
    (NULL, 'oce_ane974'),
    (NULL, 'uncomptea_3'),
    (NULL, 'moongirl_weird'),
    (NULL, 'eloize_clt'),
    (NULL, 'jaja.jmr');