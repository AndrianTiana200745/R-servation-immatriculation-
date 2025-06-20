-- Assurons-nous que la base existe
DROP DATABASE IF EXISTS reservations;
CREATE DATABASE IF NOT EXISTS reservations;
USE reservations;

-- Table Utilisateur
CREATE TABLE Utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'utilisateur') DEFAULT 'utilisateur',
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Serie
CREATE TABLE Serie(
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(4) NOT NULL UNIQUE,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('active', 'inactive') DEFAULT 'inactive'
);

-- Table Centre
CREATE TABLE Centre(
    id INT AUTO_INCREMENT PRIMARY KEY,
    designation VARCHAR(10) NOT NULL
);

-- Table Immatriculation
CREATE TABLE Immatriculation(
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) NOT NULL UNIQUE,
    centre_id INT,
    serie_id INT,
    est_reserve BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (centre_id) REFERENCES Centre(id),
    FOREIGN KEY (serie_id) REFERENCES Serie(id)
);

-- Table Reservation
CREATE TABLE Reservation(
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_reservation DATETIME DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('en attente', 'confirmee', 'annulee') DEFAULT 'en attente',
    utilisateur_id INT,
    immatriculation_id INT,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id),
    FOREIGN KEY (immatriculation_id) REFERENCES Immatriculation(id)
);

-- Insertion des centres
INSERT INTO Centre (designation) VALUES ('Ambohidahy'), ('Alhambra'), ('Antsirabe');

-- Insérer la première série : TCC
INSERT INTO Serie (code, statut) VALUES ('TCC', 'active');

-- Générer les immatriculations pour la série active
DELIMITER //

CREATE PROCEDURE generer_immatriculations_pour_serie_active()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE code_serie VARCHAR(4);
    DECLARE id_serie INT;

    -- Obtenir la série active
    SELECT id, code INTO id_serie, code_serie FROM Serie WHERE statut = 'active';

    WHILE i <= 9999 DO
        INSERT INTO Immatriculation (numero, centre_id, serie_id)
        VALUES (CONCAT(LPAD(i, 4, '0'), code_serie), 1, id_serie);
        SET i = i + 1;
    END WHILE;
END;
//

DELIMITER ;

-- Exécuter la génération pour TCC
-- CALL generer_immatriculations_pour_serie_active();
DELIMITER //

CREATE PROCEDURE changer_serie_si_terminee()
BEGIN
    DECLARE id_actuelle INT;
    DECLARE code_actuel VARCHAR(4);
    DECLARE nouvelle_serie VARCHAR(4);
    DECLARE lettre1 CHAR(1);
    DECLARE lettre2 CHAR(1);

    -- Vérifier si tous les numéros sont réservés
    SELECT id, code INTO id_actuelle, code_actuel FROM Serie WHERE statut = 'active';

    IF (SELECT COUNT(*) FROM Immatriculation WHERE serie_id = id_actuelle AND est_reserve = FALSE) = 0 THEN

        -- Désactiver la série actuelle
        UPDATE Serie SET statut = 'inactive' WHERE id = id_actuelle;

        -- Générer le code de la prochaine série
        SET lettre1 = SUBSTRING(code_actuel, 2, 1);
        SET lettre2 = SUBSTRING(code_actuel, 3, 1);

        IF lettre2 < 'Z' THEN
            SET lettre2 = CHAR(ASCII(lettre2) + 1);
        ELSE
            SET lettre2 = 'C';
            SET lettre1 = CHAR(ASCII(lettre1) + 1);
        END IF;

        SET nouvelle_serie = CONCAT('T', lettre1, lettre2);

        -- Créer la nouvelle série
        INSERT INTO Serie (code, statut) VALUES (nouvelle_serie, 'active');

        -- Générer les 0000 à 9999 pour cette nouvelle série
        CALL generer_immatriculations_pour_serie_active();
    END IF;
END;
//

DELIMITER ;
