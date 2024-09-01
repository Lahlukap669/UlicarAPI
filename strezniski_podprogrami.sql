/*CREATE FUNCTIONS*/
CREATE OR REPLACE FUNCTION create_klub(p_ime VARCHAR)
RETURNS BIGINT AS $$
DECLARE
    klub_id BIGINT;
BEGIN
    INSERT INTO Klubi (ime) VALUES (p_ime) RETURNING id INTO klub_id;
    RETURN klub_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_trener(p_ime VARCHAR, p_priimek VARCHAR, p_gmail VARCHAR, p_geslo VARCHAR, p_tel VARCHAR)
RETURNS BIGINT AS $$
DECLARE
    trener_id BIGINT;
BEGIN
    INSERT INTO Trenerji (ime, priimek, gmail, geslo, tel)
    VALUES (p_ime, p_priimek, p_gmail, p_geslo, p_tel)
    RETURNING id INTO trener_id;
    RETURN trener_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_selekcija(p_klub_id BIGINT, p_selekcija VARCHAR, p_opis TEXT)
RETURNS BIGINT AS $$
DECLARE
    selekcija_id BIGINT;
BEGIN
    INSERT INTO Selekcije (klub_id, selekcija, opis)
    VALUES (p_klub_id, p_selekcija, p_opis)
    RETURNING id INTO selekcija_id;
    RETURN selekcija_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_igralec(p_selekcija_id BIGINT, p_ime VARCHAR, p_priimek VARCHAR, p_username VARCHAR, p_geslo VARCHAR, p_tel VARCHAR)
RETURNS BIGINT AS $$
DECLARE
    igralec_id BIGINT;
BEGIN
    INSERT INTO Igralci (selekcija_id, ime, priimek, username, geslo, tel)
    VALUES (p_selekcija_id, p_ime, p_priimek, p_username, p_geslo, p_tel)
    RETURNING id INTO igralec_id;
    RETURN igralec_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_trener_selekcija(p_trener_id BIGINT, p_selekcija_id BIGINT)
RETURNS BIGINT AS $$
DECLARE
    trener_selekcija_id BIGINT;
BEGIN
    INSERT INTO Trenerji_selekcije (trener_id, selekcija_id)
    VALUES (p_trener_id, p_selekcija_id)
    RETURNING id INTO trener_selekcija_id;
    RETURN trener_selekcija_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_izziv(p_selekcija_id BIGINT, p_ime VARCHAR, p_opis TEXT, p_tockovanje TEXT, p_tedenski_challenge BOOLEAN)
RETURNS BIGINT AS $$
DECLARE
    izziv_id BIGINT;
BEGIN
    INSERT INTO Izzivi (selekcija_id, ime, opis, točkovanje, tedenski_challenge)
    VALUES (p_selekcija_id, p_ime, p_opis, p_tockovanje, p_tedenski_challenge)
    RETURNING id INTO izziv_id;
    RETURN izziv_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_izziv_igralec(
    p_trener_id BIGINT, 
    p_igralec_id BIGINT, 
    p_izziv_id BIGINT, 
    p_test1 FLOAT
)
RETURNS BIGINT AS $$
DECLARE
    izziv_igralec_id BIGINT;
BEGIN
    -- Check if the combination of igralec_id and izziv_id already exists
    IF EXISTS (
        SELECT 1 
        FROM Izzivi_igralci 
        WHERE igralec_id = p_igralec_id AND izziv_id = p_izziv_id
    ) THEN
        -- Raise an exception if a duplicate is found
        RAISE EXCEPTION 'Igralec že ima meritve za ta izziv';
    ELSE
        -- If no duplicate is found, insert the new record
        INSERT INTO Izzivi_igralci (trener_id, igralec_id, izziv_id, test1, test2, score_difference)
        VALUES (p_trener_id, p_igralec_id, p_izziv_id, p_test1, NULL, NULL)
        RETURNING id INTO izziv_igralec_id;
    END IF;

    RETURN izziv_igralec_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_drugi_izziv(p_ime VARCHAR, p_url VARCHAR)
RETURNS BIGINT AS $$
DECLARE
    drugi_izziv_id BIGINT;
BEGIN
    INSERT INTO Drugi_izzivi (ime, url)
    VALUES (p_ime, p_url)
    RETURNING id INTO drugi_izziv_id;
    RETURN drugi_izziv_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_drugi_izziv_igralec(p_drug_izziv_id BIGINT, p_igralec_id BIGINT, p_trener_id BIGINT)
RETURNS BIGINT AS $$
DECLARE
    drugi_izziv_igralec_id BIGINT;
BEGIN
    INSERT INTO Drugi_izzivi_igralci (drug_izziv_id, igralec_id, trener_id, tocke, photo_score, approved)
    VALUES (p_drug_izziv_id, p_igralec_id, p_trener_id, NULL, NULL, FALSE)
    RETURNING id INTO drugi_izziv_igralec_id;
    RETURN drugi_izziv_igralec_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_registracija(
    p_ime VARCHAR, 
    p_priimek VARCHAR, 
    p_geslo VARCHAR, 
    p_username VARCHAR, 
    p_tel VARCHAR, 
    p_kraj_kluba VARCHAR, 
    p_selekcija_id BIGINT, 
    p_tip VARCHAR
)
RETURNS BIGINT AS $$
DECLARE
    registracija_id BIGINT;
    v_exists BOOLEAN;
BEGIN
    -- Check if the username already exists
    SELECT EXISTS (
        SELECT 1 FROM Registracija WHERE username = p_username
    ) INTO v_exists;

    IF v_exists THEN
        -- Raise an exception or return a specific value indicating that the username is taken
        RAISE EXCEPTION 'Username already exists';
    ELSE
        -- Insert the new registration if the username is not taken
        INSERT INTO Registracija (
            ime, priimek, geslo, username, tel, kraj_kluba, selekcija_id, tip, status
        )
        VALUES (
            p_ime, p_priimek, p_geslo, p_username, p_tel, p_kraj_kluba, p_selekcija_id, p_tip, 'pending'
        )
        RETURNING id INTO registracija_id;
        
        RETURN registracija_id;
    END IF;
END;
$$ LANGUAGE plpgsql;


/*UPDATE FUNCTIONS*/
CREATE OR REPLACE FUNCTION update_klub(p_klub_id BIGINT, p_ime VARCHAR)
RETURNS VOID AS $$
BEGIN
    UPDATE Klubi
    SET ime = p_ime
    WHERE id = p_klub_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_trener(p_trener_id BIGINT, p_ime VARCHAR, p_priimek VARCHAR, p_gmail VARCHAR, p_geslo VARCHAR, p_tel VARCHAR)
RETURNS VOID AS $$
BEGIN
    UPDATE Trenerji
    SET ime = p_ime, priimek = p_priimek, gmail = p_gmail, geslo = p_geslo, tel = p_tel
    WHERE id = p_trener_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_selekcija(p_selekcija_id BIGINT, p_klub_id BIGINT, p_selekcija VARCHAR, p_opis TEXT)
RETURNS VOID AS $$
BEGIN
    UPDATE Selekcije
    SET klub_id = p_klub_id, selekcija = p_selekcija, opis = p_opis
    WHERE id = p_selekcija_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_igralec(p_igralec_id BIGINT, p_selekcija_id BIGINT, p_ime VARCHAR, p_priimek VARCHAR, p_username VARCHAR, p_geslo VARCHAR, p_tel VARCHAR, p_score FLOAT)
RETURNS VOID AS $$
BEGIN
    UPDATE Igralci
    SET selekcija_id = p_selekcija_id, ime = p_ime, priimek = p_priimek, username = p_username, geslo = p_geslo, tel = p_tel, score = p_score
    WHERE id = p_igralec_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_trener_selekcija(p_trener_selekcija_id BIGINT, p_trener_id BIGINT, p_selekcija_id BIGINT)
RETURNS VOID AS $$
BEGIN
    UPDATE Trenerji_selekcije
    SET trener_id = p_trener_id, selekcija_id = p_selekcija_id
    WHERE id = p_trener_selekcija_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_izziv(p_izziv_id BIGINT, p_selekcija_id BIGINT, p_ime VARCHAR, p_opis TEXT, p_točkovanje TEXT, p_tedenski_challenge BOOLEAN)
RETURNS VOID AS $$
BEGIN
    UPDATE Izzivi
    SET selekcija_id = p_selekcija_id, ime = p_ime, opis = p_opis, točkovanje = p_točkovanje, tedenski_challenge = p_tedenski_challenge
    WHERE id = p_izziv_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_izziv_igralec(p_izziv_igralec_id BIGINT, p_trener_id BIGINT, p_igralec_id BIGINT, p_izziv_id BIGINT, p_test1 FLOAT, p_test2 FLOAT)
RETURNS VOID AS $$
BEGIN
    UPDATE Izzivi_igralci
    SET trener_id = p_trener_id, igralec_id = p_igralec_id, izziv_id = p_izziv_id, test1 = p_test1, test2 = p_test2, score_difference = p_test2 - p_test1
    WHERE id = p_izziv_igralec_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_drugi_izziv(p_drugi_izziv_id BIGINT, p_ime VARCHAR, p_url VARCHAR)
RETURNS VOID AS $$
BEGIN
    UPDATE Drugi_izzivi
    SET ime = p_ime, url = p_url
    WHERE id = p_drugi_izziv_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_drugi_izziv_igralec(p_drugi_izziv_igralec_id BIGINT, p_drug_izziv_id BIGINT, p_igralec_id BIGINT, p_trener_id BIGINT, p_tocke FLOAT, p_photo_score FLOAT, p_approved BOOLEAN)
RETURNS VOID AS $$
BEGIN
    UPDATE Drugi_izzivi_igralci
    SET drug_izziv_id = p_drug_izziv_id, igralec_id = p_igralec_id, trener_id = p_trener_id, tocke = p_tocke, photo_score = p_photo_score, approved = p_approved
    WHERE id = p_drugi_izziv_igralec_id;
END;
$$ LANGUAGE plpgsql;

/*DELETE FUNCTIONS*/
CREATE OR REPLACE FUNCTION delete_klub(p_klub_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM Klubi
    WHERE id = p_klub_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_trener(p_trener_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM Trenerji
    WHERE id = p_trener_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_selekcija(p_selekcija_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM Selekcije
    WHERE id = p_selekcija_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_igralec(p_igralec_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM Igralci
    WHERE id = p_igralec_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_trener_selekcija(p_trener_selekcija_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM Trenerji_selekcije
    WHERE id = p_trener_selekcija_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_izziv(p_izziv_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    -- First, delete all related records from the Izzivi_igralci table
    DELETE FROM Izzivi_igralci
    WHERE izziv_id = p_izziv_id;

    -- Then, delete the record from the Izzivi table
    DELETE FROM Izzivi
    WHERE id = p_izziv_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION delete_izziv_igralec(p_izziv_igralec_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM Izzivi_igralci
    WHERE id = p_izziv_igralec_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_drugi_izziv(p_drugi_izziv_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM Drugi_izzivi
    WHERE id = p_drugi_izziv_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_drugi_izziv_igralec(p_drugi_izziv_igralec_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM Drugi_izzivi_igralci
    WHERE id = p_drugi_izziv_igralec_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

/*RETRIEVE FUNCTIONS*/
CREATE OR REPLACE FUNCTION get_all_selekcije_by_klub_id(p_klub_id BIGINT)
RETURNS TABLE(id BIGINT, selekcija VARCHAR, opis TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, selekcija, opis
    FROM Selekcije
    WHERE klub_id = p_klub_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_igralci_by_selekcija_id(p_selekcija_id BIGINT)
RETURNS TABLE(id BIGINT, ime VARCHAR, priimek VARCHAR, username VARCHAR, tel VARCHAR, score FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, ime, priimek, username, tel, score
    FROM Igralci
    WHERE selekcija_id = p_selekcija_id;
END;
$$ LANGUAGE plpgsql;

-- GET DATA BY ID
CREATE OR REPLACE FUNCTION get_trener_by_id(p_trener_id BIGINT)
RETURNS TABLE(trenerji_id BIGINT, ime VARCHAR, priimek VARCHAR, gmail VARCHAR, tel VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT Trenerji.id, Trenerji.ime, Trenerji.priimek, Trenerji.gmail, Trenerji.tel
    FROM Trenerji
    WHERE Trenerji.id = p_trener_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_izzivi_igralci_by_izziv_id(p_izziv_id BIGINT)
RETURNS TABLE(
    izzivi_igralci_id BIGINT,
    trener_id BIGINT,
    igralec_id BIGINT,
    izziv_id BIGINT,
    test1 FLOAT,
    test2 FLOAT,
    score_difference FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        Izzivi_igralci.id AS izzivi_igralci_id,
        Izzivi_igralci.trener_id,
        Izzivi_igralci.igralec_id,
        Izzivi_igralci.izziv_id,
        Izzivi_igralci.test1,
        Izzivi_igralci.test2,
        Izzivi_igralci.score_difference
    FROM Izzivi_igralci
    WHERE Izzivi_igralci.izziv_id = p_izziv_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_igralec_by_id(p_igralec_id BIGINT)
RETURNS TABLE(igralci_id BIGINT, selekcija_id BIGINT, ime VARCHAR, priimek VARCHAR, username VARCHAR, tel VARCHAR, score FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT Igralci.id, Igralci.selekcija_id, Igralci.ime, Igralci.priimek, Igralci.username, Igralci.tel, Igralci.score
    FROM Igralci
    WHERE Igralci.id = p_igralec_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_izzivi_by_selekcija_id(p_selekcija_id BIGINT)
RETURNS TABLE(
    izzivi_id BIGINT,
    selekcija_id BIGINT,
    ime VARCHAR,
    opis TEXT,
    točkovanje TEXT,
    tedenski_challenge BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT id AS izzivi_id, selekcija_id, ime, opis, točkovanje, tedenski_challenge
    FROM Izzivi
    WHERE selekcija_id = p_selekcija_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_trenerji_selekcije_by_trener_id(p_trener_id BIGINT)
RETURNS TABLE(
    trener_selekcija_id BIGINT,
    trenerji_selekcije_trener_id BIGINT,
    selekcija_id BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT ts.id AS trener_selekcija_id, ts.trener_id AS trenerji_selekcije_trener_id, ts.selekcija_id
    FROM Trenerji_selekcije ts
    WHERE ts.trener_id = p_trener_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_selekcija_by_id(p_selekcija_id BIGINT)
RETURNS TABLE(selekcije_id BIGINT, klub_id BIGINT, selekcija VARCHAR, opis TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT Selekcije.id, Selekcije.klub_id, Selekcije.selekcija, Selekcije.opis
    FROM Selekcije
    WHERE Selekcije.id = p_selekcija_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_selekcije_by_klub_id(p_klub_id BIGINT)
RETURNS TABLE(selekcija_id BIGINT, selekcija_name VARCHAR, selekcija_opis TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT Selekcije.id AS selekcija_id, Selekcije.selekcija AS selekcija_name, Selekcije.opis AS selekcija_opis
    FROM Selekcije
    WHERE Selekcije.klub_id = p_klub_id::BIGINT;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_klub_by_id(p_klub_id BIGINT)
RETURNS TABLE(klubi_id BIGINT, ime VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT Klubi.id, Klubi.ime
    FROM Klubi
    WHERE Klubi.id = p_klub_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_izziv_by_id(p_izziv_id BIGINT)
RETURNS TABLE(izzivi_id BIGINT, selekcija_id BIGINT, ime VARCHAR, opis TEXT, tockovanje TEXT, tedenski_challenge BOOLEAN) AS $$
BEGIN
    RETURN QUERY
    SELECT Izzivi.id, Izzivi.selekcija_id, Izzivi.ime, Izzivi.opis, Izzivi.tockovanje, Izzivi.tedenski_challenge
    FROM Izzivi
    WHERE Izzivi.id = p_izziv_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_drugi_izziv_by_id(p_drugi_izziv_id BIGINT)
RETURNS TABLE(drugi_izzivi_id BIGINT, ime VARCHAR, url VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT Drugi_izzivi.id, Drugi_izzivi.ime, Drugi_izzivi.url
    FROM Drugi_izzivi
    WHERE Drugi_izzivi.id = p_drugi_izziv_id;
END;
$$ LANGUAGE plpgsql;

/*GET ALL DATA FUNCTIONS*/
CREATE OR REPLACE FUNCTION get_all_klubi()
RETURNS TABLE(id BIGINT, ime VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT Klubi.id, Klubi.ime
    FROM Klubi;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_trenerji()
RETURNS TABLE(id BIGINT, ime VARCHAR, priimek VARCHAR, gmail VARCHAR, tel VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT Trenerji.id, Trenerji.ime, Trenerji.priimek, Trenerji.gmail, Trenerji.tel
    FROM Trenerji;
END;
$$ LANGUAGE plpgsql;

/*USELESS*/
CREATE OR REPLACE FUNCTION get_all_selekcije()
RETURNS TABLE(id BIGINT, klub_id BIGINT, selekcija VARCHAR, opis TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, klub_id, selekcija, opis
    FROM Selekcije;
END;
$$ LANGUAGE plpgsql;

/*USELESS*/
CREATE OR REPLACE FUNCTION get_all_igralci()
RETURNS TABLE(id BIGINT, selekcija_id BIGINT, ime VARCHAR, priimek VARCHAR, username VARCHAR, tel VARCHAR, score FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, selekcija_id, ime, priimek, username, tel, score
    FROM Igralci;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_izzivi()
RETURNS TABLE(izzivi_id BIGINT, selekcija_id BIGINT, ime VARCHAR, opis TEXT, točkovanje TEXT, tedenski_challenge BOOLEAN) AS $$
BEGIN
    RETURN QUERY
    SELECT Izzivi.id, Izzivi.selekcija_id, Izzivi.ime, Izzivi.opis, Izzivi.točkovanje, Izzivi.tedenski_challenge
    FROM Izzivi
    ORDER BY Izzivi.id DESC -- Most recent entries first
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;


-- Function for get_all_izzivi_igralci grouped by selekcija_id
CREATE OR REPLACE FUNCTION get_all_izzivi_igralci_by_selekcija(p_selekcija_id BIGINT)
RETURNS TABLE(id BIGINT, trener_id BIGINT, igralec_id BIGINT, izziv_id BIGINT, test1 FLOAT, test2 FLOAT, score_difference FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT Izzivi_igralci.id, Izzivi_igralci.trener_id, Izzivi_igralci.igralec_id, Izzivi_igralci.izziv_id, Izzivi_igralci.test1, Izzivi_igralci.test2, Izzivi_igralci.score_difference
    FROM Izzivi_igralci
    INNER JOIN Izzivi ON Izzivi.id = Izzivi_igralci.izziv_id
    WHERE Izzivi.selekcija_id = p_selekcija_id;
END;
$$ LANGUAGE plpgsql;

-- Function for get_all_drugi_izzivi grouped by selekcija_id
CREATE OR REPLACE FUNCTION get_all_drugi_izzivi_by_selekcija(p_selekcija_id BIGINT)
RETURNS TABLE(id BIGINT, ime VARCHAR, url VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT Drugi_izzivi.id, Drugi_izzivi.ime, Drugi_izzivi.url
    FROM Drugi_izzivi
    INNER JOIN Drugi_izzivi_igralci ON Drugi_izzivi_igralci.drug_izziv_id = Drugi_izzivi.id
    INNER JOIN Igralci ON Igralci.id = Drugi_izzivi_igralci.igralec_id
    WHERE Igralci.selekcija_id = p_selekcija_id;
END;
$$ LANGUAGE plpgsql;



-- Function for get_all_drugi_izzivi_igralci grouped by selekcija_id
CREATE OR REPLACE FUNCTION get_all_drugi_izzivi_igralci_by_selekcija(p_selekcija_id BIGINT)
RETURNS TABLE(id BIGINT, drug_izziv_id BIGINT, igralec_id BIGINT, trener_id BIGINT, tocke FLOAT, photo_score FLOAT, approved BOOLEAN) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        Drugi_izzivi_igralci.id, 
        Drugi_izzivi_igralci.drug_izziv_id, 
        Drugi_izzivi_igralci.igralec_id, 
        Drugi_izzivi_igralci.trener_id, 
        Drugi_izzivi_igralci.tocke, 
        Drugi_izzivi_igralci.photo_score, 
        Drugi_izzivi_igralci.approved
    FROM 
        Drugi_izzivi_igralci
    INNER JOIN 
        Igralci ON Igralci.id = Drugi_izzivi_igralci.igralec_id
    WHERE 
        Igralci.selekcija_id = p_selekcija_id;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_all_registracije()
RETURNS TABLE(id BIGINT, ime VARCHAR, priimek VARCHAR, username VARCHAR, tel VARCHAR, kraj_kluba VARCHAR, selekcija_id BIGINT, status VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT Registracija.id, Registracija.ime, Registracija.priimek, Registracija.username, Registracija.tel, Registracija.kraj_kluba, Registracija.selekcija_id, Registracija.status
    FROM Registracija;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_registracije_no()
RETURNS TABLE(id BIGINT, ime VARCHAR, priimek VARCHAR, username VARCHAR, tel VARCHAR, kraj_kluba VARCHAR, selekcija_id BIGINT, status VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT Registracija.id, Registracija.ime, Registracija.priimek, Registracija.username, Registracija.tel, Registracija.kraj_kluba, Registracija.selekcija_id, Registracija.status
    FROM Registracija
    WHERE Registracija.status = 'pending';
END;
$$ LANGUAGE plpgsql;

/*OTHER FUNCTIONS*/
CREATE OR REPLACE FUNCTION approve_registracija(p_registracija_id BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    v_ime VARCHAR;
    v_priimek VARCHAR;
    v_geslo VARCHAR;
    v_username VARCHAR;
    v_tel VARCHAR;
    v_kraj_kluba VARCHAR;
    v_selekcija_id BIGINT;
    v_tip VARCHAR;
    v_status VARCHAR;
BEGIN
    -- Fetch registration data
    SELECT ime, priimek, geslo, username, tel, kraj_kluba, selekcija_id, tip, status
    INTO v_ime, v_priimek, v_geslo, v_username, v_tel, v_kraj_kluba, v_selekcija_id, v_tip, v_status
    FROM Registracija
    WHERE id = p_registracija_id;

    -- Check if the status is pending
    IF v_status = 'pending' THEN
        -- Approve registration and create a player or coach
        IF v_tip = 'igralec' THEN
            -- Insert into Igralci table
            PERFORM create_igralec(v_selekcija_id, v_ime, v_priimek, v_username, v_geslo, v_tel);
        ELSIF v_tip = 'trener' THEN
            -- Insert into Trenerji table
            PERFORM create_trener(v_ime, v_priimek, v_username, v_geslo, v_tel);
        ELSE
            RAISE EXCEPTION 'Neveljaven tip uporabnika.';
        END IF;

        -- Update registration status to approved
        UPDATE Registracija
        SET status = 'approved'
        WHERE id = p_registracija_id;

        RETURN TRUE;

    ELSE
        -- Return FALSE if registration was already processed
        RETURN FALSE;
    END IF;
EXCEPTION WHEN OTHERS THEN
    -- Handle any other errors
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

/*USELESS*/
CREATE OR REPLACE FUNCTION calculate_score_difference(p_izziv_igralec_id BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    v_test1 FLOAT;
    v_test2 FLOAT;
    v_score_difference FLOAT;
BEGIN
    -- Pridobitev testnih rezultatov
    SELECT test1, test2
    INTO v_test1, v_test2
    FROM Izzivi_igralci
    WHERE id = p_izziv_igralec_id;

    -- Izračun razlike med testoma
    v_score_difference = v_test2 - v_test1;

    -- Posodobitev razlike v tabeli
    UPDATE Izzivi_igralci
    SET score_difference = v_score_difference
    WHERE id = p_izziv_igralec_id;

    RETURN TRUE;
EXCEPTION WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

/*USELESS*/
CREATE OR REPLACE FUNCTION award_nagrada(p_izziv_id BIGINT)
RETURNS BIGINT AS $$
DECLARE
    v_winner_id BIGINT;
BEGIN
    -- Pridobitev igralca z najvišjimi točkami v izzivu
    SELECT igralec_id
    INTO v_winner_id
    FROM Izzivi_igralci
    WHERE izziv_id = p_izziv_id
    ORDER BY score_difference DESC
    LIMIT 1;

    -- Če je zmagovalec najden, vrni ID, drugače vrni NULL
    IF v_winner_id IS NOT NULL THEN
        RETURN v_winner_id;
    ELSE
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_leaderboard_by_selekcija(p_selekcija_id BIGINT)
RETURNS TABLE(
    rank INT,
    igralec_id BIGINT,
    ime VARCHAR,
    priimek VARCHAR,
    username VARCHAR,
    total_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        RANK() OVER (ORDER BY score DESC) AS rank,
        id AS igralec_id,
        ime,
        priimek,
        username,
        score AS total_score
    FROM 
        Igralci
    WHERE 
        selekcija_id = p_selekcija_id
    ORDER BY 
        total_score DESC;
END;
$$ LANGUAGE plpgsql;

-- LOGIN CHECKS
CREATE OR REPLACE FUNCTION login_trenerji(p_email VARCHAR, p_hashed_password VARCHAR)
RETURNS BIGINT AS $$
DECLARE
    v_trener_id BIGINT;
BEGIN
    -- Check if the email and hashed password exist in Trenerji and return the ID
    SELECT id
    INTO v_trener_id
    FROM Trenerji
    WHERE gmail = p_email AND geslo = p_hashed_password;

    RETURN v_trener_id;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION login_igralci(p_username VARCHAR, p_hashed_password VARCHAR)
RETURNS BIGINT AS $$
DECLARE
    v_igralec_id BIGINT;
BEGIN
    -- Check if the username and hashed password exist in Igralci and return the ID
    SELECT id
    INTO v_igralec_id
    FROM Igralci
    WHERE username = p_username AND geslo = p_hashed_password;

    RETURN v_igralec_id;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_total_score_after_izzivi_igralci_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Recalculate the total score for the player in Igralci table
    UPDATE Igralci
    SET score = (
        SELECT COALESCE(SUM(score_difference), 0)
        FROM Izzivi_igralci
        WHERE igralec_id = NEW.igralec_id
    ) + (
        SELECT COALESCE(SUM(tocke), 0)
        FROM Drugi_izzivi_igralci
        WHERE igralec_id = NEW.igralec_id
    )
    WHERE id = NEW.igralec_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_total_score_after_izzivi_igralci
AFTER INSERT OR UPDATE ON Izzivi_igralci
FOR EACH ROW
EXECUTE FUNCTION update_total_score_after_izzivi_igralci_change();

CREATE TRIGGER trg_update_total_score_after_drugi_izzivi_igralci
AFTER INSERT OR UPDATE ON Drugi_izzivi_igralci
FOR EACH ROW
EXECUTE FUNCTION update_total_score_after_izzivi_igralci_change();
