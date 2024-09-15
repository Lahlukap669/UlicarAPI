DROP TABLE IF EXISTS Klubi CASCADE;
DROP TABLE IF EXISTS Trenerji CASCADE;
DROP TABLE IF EXISTS Selekcije CASCADE;
DROP TABLE IF EXISTS Igralci CASCADE;
DROP TABLE IF EXISTS Trenerji_selekcije CASCADE;
DROP TABLE IF EXISTS Izzivi CASCADE;
DROP TABLE IF EXISTS Izzivi_igralci CASCADE;
DROP TABLE IF EXISTS Drugi_izzivi CASCADE;
DROP TABLE IF EXISTS Drugi_izzivi_igralci CASCADE;
DROP TABLE IF EXISTS Registracija CASCADE;

CREATE TABLE Trenerji (
    id BIGSERIAL PRIMARY KEY,
    ime VARCHAR NOT NULL,
    priimek VARCHAR NOT NULL,
    gmail VARCHAR NOT NULL UNIQUE,
    geslo VARCHAR NOT NULL,
    tel VARCHAR
);

CREATE TABLE Klubi (
    id BIGSERIAL PRIMARY KEY,
    ime VARCHAR NOT NULL
);

CREATE TABLE Selekcije (
    id BIGSERIAL PRIMARY KEY,
    klub_id BIGINT REFERENCES Klubi(id),
    selekcija VARCHAR NOT NULL,
    opis TEXT
);

CREATE TABLE Igralci (
    id BIGSERIAL PRIMARY KEY,
    selekcija_id BIGINT REFERENCES Selekcije(id),
    ime VARCHAR NOT NULL,
    priimek VARCHAR NOT NULL,
    username VARCHAR NOT NULL UNIQUE,
    geslo VARCHAR NOT NULL,
    tel VARCHAR,
    score FLOAT
);

CREATE TABLE Trenerji_selekcije (
    id BIGSERIAL PRIMARY KEY,
    trener_id BIGINT REFERENCES Trenerji(id),
    selekcija_id BIGINT REFERENCES Selekcije(id)
);

CREATE TABLE Izzivi (
    id BIGSERIAL PRIMARY KEY,
    selekcija_id BIGINT REFERENCES Selekcije(id),
    ime VARCHAR NOT NULL,
    opis TEXT,
    točkovanje TEXT,
    tedenski_challenge BOOLEAN
);

CREATE TABLE Izzivi_igralci (
    id BIGSERIAL PRIMARY KEY,
    trener_id BIGINT REFERENCES Trenerji(id),
    igralec_id BIGINT REFERENCES Igralci(id),
    izziv_id BIGINT REFERENCES Izzivi(id),
    test1 FLOAT,
    test2 FLOAT,
    score_difference FLOAT
);

CREATE TABLE Drugi_izzivi (
    id BIGSERIAL PRIMARY KEY,
    ime VARCHAR NOT NULL,
    url VARCHAR
);

CREATE TABLE Drugi_izzivi_igralci (
    id BIGSERIAL PRIMARY KEY,
    drug_izziv_id BIGINT REFERENCES Drugi_izzivi(id),
    igralec_id BIGINT REFERENCES Igralci(id),
    trener_id BIGINT REFERENCES Trenerji(id),
    tocke FLOAT,
    photo_score FLOAT,
    approved_by BIGINT REFERENCES Trenerji(id),
    approved BOOLEAN
);

CREATE TABLE Registracija (
    id BIGSERIAL PRIMARY KEY,
    ime VARCHAR NOT NULL,
    priimek VARCHAR NOT NULL,
    geslo VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    tel VARCHAR,
    kraj_kluba VARCHAR,
    selekcija_id BIGINT REFERENCES Selekcije(id),
    status VARCHAR NOT NULL
);

ALTER TABLE Registracija
ADD COLUMN tip VARCHAR NOT NULL CHECK (tip IN ('igralec', 'trener'));
