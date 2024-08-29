from flask import Flask, jsonify, request, send_file, send_from_directory
import json
import hashlib
from flask_cors import CORS
import os

app = Flask(__name__)

from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ketsqoxt:fcQSl8LgKt181nmEcPfazzY_oIYBsRQh@abul.db.elephantsql.com/ketsqoxt"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

## TESTING
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        podatki_json = request.get_json()
        print(podatki_json["username"])
        return jsonify({'ime': podatki_json["username"]}), 201
    else:
        return jsonify({'u sent': "nothing"})

## REGISTRATION
@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        podatki_json = request.get_json()
        
        # Extracting sent data
        Fname = podatki_json.get("FirstName")
        Lname = podatki_json.get("LastName")
        username = podatki_json.get("username")
        password = podatki_json.get("password")
        tel = podatki_json.get("tel")
        kraj_kluba = podatki_json.get("kraj_kluba")
        selekcija_id = podatki_json.get("selekcija_id", None)  # Default to None if not provided
        tip = podatki_json.get("tip")  # Extract the role (e.g., "trener" or "igralec")
        
        # Hashing the password
        password_h = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Database interaction
        try:
            # Call the create_registracija function from the database
            query = text("""
                SELECT create_registracija(
                    :Fname, 
                    :Lname, 
                    :password_h, 
                    :username, 
                    :tel, 
                    :kraj_kluba, 
                    :selekcija_id,
                    :tip
                )
            """)
            r = db.session.execute(query, {
                'Fname': Fname, 
                'Lname': Lname, 
                'password_h': password_h, 
                'username': username, 
                'tel': tel, 
                'kraj_kluba': kraj_kluba, 
                'selekcija_id': selekcija_id,
                'tip': tip
            }).scalar()

            db.session.commit()
            
            # Return success response
            return jsonify({'success': True, 'registracija_id': r}), 201
        
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405


## CREATE CLUB
@app.route("/create_klub", methods=['POST'])
def create_klub():
    if request.method == 'POST':
        podatki_json = request.get_json()

        # Extracting the club name from the request
        K_ime = podatki_json.get("klub_ime")

        # Database interaction to create a new club
        try:
            query = text("SELECT create_klub(:klub_ime)")
            klub_id = db.session.execute(query, {'klub_ime': K_ime}).scalar()

            db.session.commit()

            # Return success response with the new club ID
            return jsonify({'success': True, 'klub_id': klub_id}), 201

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## CREATE SELECTION
@app.route("/create_selekcija", methods=['POST'])
def create_selekcija():
    if request.method == 'POST':
        podatki_json = request.get_json()

        # Extracting selection details from the request
        klub_id = podatki_json.get("klub_id")
        selekcija_ime = podatki_json.get("selekcija_ime")
        opis = podatki_json.get("opis", "")  # Description is optional, default to empty string

        # Database interaction to create a new selection
        try:
            query = text("""
                SELECT create_selekcija(:klub_id, :selekcija_ime, :opis)
            """)
            selekcija_id = db.session.execute(query, {
                'klub_id': klub_id,
                'selekcija_ime': selekcija_ime,
                'opis': opis
            }).scalar()

            db.session.commit()

            # Return success response with the new selection ID
            return jsonify({'success': True, 'selekcija_id': selekcija_id}), 201

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## CREATE TRAINER -SELECTION CONNECTION
@app.route("/create_trener_selekcija", methods=['POST'])
def create_trener_selekcija():
    if request.method == 'POST':
        try:
            # Extract the trainer and selection IDs from the request data
            podatki_json = request.get_json()
            trener_id = podatki_json.get("trener_id")
            selekcija_id = podatki_json.get("selekcija_id")

            # Call the create_trener_selekcija function in the database
            query = text("""
                SELECT create_trener_selekcija(:trener_id, :selekcija_id)
            """)
            trener_selekcija_id = db.session.execute(query, {
                'trener_id': trener_id,
                'selekcija_id': selekcija_id
            }).scalar()

            db.session.commit()

            # Return success response with the new trener_selekcija_id
            return jsonify({'success': True, 'trener_selekcija_id': trener_selekcija_id}), 201

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

##CREATE IZZIV
@app.route("/create_izziv", methods=['POST'])
def create_izziv():
    if request.method == 'POST':
        try:
            # Extract the challenge details from the request data
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")
            ime = podatki_json.get("ime")
            opis = podatki_json.get("opis")
            tockovanje = podatki_json.get("tockovanje")
            tedenski_challenge = podatki_json.get("tedenski_challenge")

            # Call the create_izziv function in the database
            query = text("""
                SELECT create_izziv(:selekcija_id, :ime, :opis, :tockovanje, :tedenski_challenge)
            """)
            izziv_id = db.session.execute(query, {
                'selekcija_id': selekcija_id,
                'ime': ime,
                'opis': opis,
                'tockovanje': tockovanje,
                'tedenski_challenge': tedenski_challenge
            }).scalar()

            db.session.commit()

            # Return success response with the new izziv_id
            return jsonify({'success': True, 'izziv_id': izziv_id}), 201

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

##CREATE IZZIV_IGRALEC CONNECTION
@app.route("/create_izziv_igralec", methods=['POST'])
def create_izziv_igralec():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            trener_id = podatki_json.get("trener_id")
            igralec_id = podatki_json.get("igralec_id")
            izziv_id = podatki_json.get("izziv_id")
            test1 = podatki_json.get("test1")

            # Call the create_izziv_igralec function in the database
            query = text("""
                SELECT create_izziv_igralec(:trener_id, :igralec_id, :izziv_id, :test1)
            """)
            izziv_igralec_id = db.session.execute(query, {
                'trener_id': trener_id,
                'igralec_id': igralec_id,
                'izziv_id': izziv_id,
                'test1': test1
            }).scalar()

            db.session.commit()

            # Return success response with the new izziv_igralec_id
            return jsonify({'success': True, 'izziv_igralec_id': izziv_igralec_id}), 201

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## CREATE DRUGI_IZZIV
@app.route("/create_drugi_izziv", methods=['POST'])
def create_drugi_izziv():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            ime = podatki_json.get("ime")
            url = podatki_json.get("url")

            # Call the create_drugi_izziv function in the database
            query = text("""
                SELECT create_drugi_izziv(:ime, :url)
            """)
            drugi_izziv_id = db.session.execute(query, {
                'ime': ime,
                'url': url
            }).scalar()

            db.session.commit()

            # Return success response with the new drugi_izziv_id
            return jsonify({'success': True, 'drugi_izziv_id': drugi_izziv_id}), 201

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## CREATE DRUGI_IZZIV_IGRALEC CONNECTION
@app.route("/create_drugi_izziv_igralec", methods=['POST'])
def create_drugi_izziv_igralec():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            drug_izziv_id = podatki_json.get("drug_izziv_id")
            igralec_id = podatki_json.get("igralec_id")
            trener_id = podatki_json.get("trener_id")

            # Call the create_drugi_izziv_igralec function in the database
            query = text("""
                SELECT create_drugi_izziv_igralec(:drug_izziv_id, :igralec_id, :trener_id)
            """)
            drugi_izziv_igralec_id = db.session.execute(query, {
                'drug_izziv_id': drug_izziv_id,
                'igralec_id': igralec_id,
                'trener_id': trener_id
            }).scalar()

            db.session.commit()

            # Return success response with the new drugi_izziv_igralec_id
            return jsonify({'success': True, 'drugi_izziv_igralec_id': drugi_izziv_igralec_id}), 201

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405



## APPROVE REGISTRATION
@app.route("/approve_registration", methods=['POST'])
def approve_registration():
    if request.method == 'POST':
        try:
            # Extract the registration ID from the request data
            podatki_json = request.get_json()
            registracija_id = podatki_json["registracija_id"]

            # Call the approve_registracija function in the database
            query = text("SELECT approve_registracija(:registracija_id)")
            r = db.session.execute(query, {'registracija_id': registracija_id}).scalar()

            db.session.commit()

            # Check if the approval was successful
            if r:
                return jsonify({'success': True, 'message': 'Registration approved successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Approval failed or registration already processed'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## UPDATE KLUB
@app.route("/update_klub", methods=['POST'])
def update_klub():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            klub_id = podatki_json.get("klub_id")
            ime = podatki_json.get("ime")

            # Call the update_klub function in the database
            query = text("""
                SELECT update_klub(:klub_id, :ime)
            """)
            db.session.execute(query, {
                'klub_id': klub_id,
                'ime': ime
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Club name updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

##UPDATE TRENER
import hashlib

@app.route("/update_trener", methods=['POST'])
def update_trener():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            trener_id = podatki_json.get("trener_id")
            ime = podatki_json.get("ime")
            priimek = podatki_json.get("priimek")
            gmail = podatki_json.get("gmail")
            geslo = podatki_json.get("geslo")
            tel = podatki_json.get("tel")

            # Hash the password before storing it
            hashed_geslo = hashlib.sha256(geslo.encode('utf-8')).hexdigest()

            # Call the update_trener function in the database
            query = text("""
                SELECT update_trener(:trener_id, :ime, :priimek, :gmail, :hashed_geslo, :tel)
            """)
            db.session.execute(query, {
                'trener_id': trener_id,
                'ime': ime,
                'priimek': priimek,
                'gmail': gmail,
                'hashed_geslo': hashed_geslo,
                'tel': tel
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Coach details updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## UPDATE SELEKCIJA
@app.route("/update_selekcija", methods=['POST'])
def update_selekcija():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")
            klub_id = podatki_json.get("klub_id")
            selekcija = podatki_json.get("selekcija")
            opis = podatki_json.get("opis")

            # Call the update_selekcija function in the database
            query = text("""
                SELECT update_selekcija(:selekcija_id, :klub_id, :selekcija, :opis)
            """)
            db.session.execute(query, {
                'selekcija_id': selekcija_id,
                'klub_id': klub_id,
                'selekcija': selekcija,
                'opis': opis
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Selection updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

##UPDATE IGRALEC
import hashlib

@app.route("/update_igralec", methods=['POST'])
def update_igralec():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            igralec_id = podatki_json.get("igralec_id")
            selekcija_id = podatki_json.get("selekcija_id")
            ime = podatki_json.get("ime")
            priimek = podatki_json.get("priimek")
            username = podatki_json.get("username")
            geslo = podatki_json.get("geslo")
            tel = podatki_json.get("tel")
            score = podatki_json.get("score")

            # Hash the password before storing it
            hashed_geslo = hashlib.sha256(geslo.encode('utf-8')).hexdigest()

            # Call the update_igralec function in the database
            query = text("""
                SELECT update_igralec(:igralec_id, :selekcija_id, :ime, :priimek, :username, :hashed_geslo, :tel, :score)
            """)
            db.session.execute(query, {
                'igralec_id': igralec_id,
                'selekcija_id': selekcija_id,
                'ime': ime,
                'priimek': priimek,
                'username': username,
                'hashed_geslo': hashed_geslo,
                'tel': tel,
                'score': score
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Player details updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## UPDATE TRENER_SELEKCIJA CONNECTION
@app.route("/update_trener_selekcija", methods=['POST'])
def update_trener_selekcija():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            trener_selekcija_id = podatki_json.get("trener_selekcija_id")
            trener_id = podatki_json.get("trener_id")
            selekcija_id = podatki_json.get("selekcija_id")

            # Call the update_trener_selekcija function in the database
            query = text("""
                SELECT update_trener_selekcija(:trener_selekcija_id, :trener_id, :selekcija_id)
            """)
            db.session.execute(query, {
                'trener_selekcija_id': trener_selekcija_id,
                'trener_id': trener_id,
                'selekcija_id': selekcija_id
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Coach-Selection association updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## UPDATE IZZIV
@app.route("/update_izziv", methods=['POST'])
def update_izziv():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            izziv_id = podatki_json.get("izziv_id")
            selekcija_id = podatki_json.get("selekcija_id")
            ime = podatki_json.get("ime")
            opis = podatki_json.get("opis")
            tockovanje = podatki_json.get("točkovanje")
            tedenski_challenge = podatki_json.get("tedenski_challenge")

            # Call the update_izziv function in the database
            query = text("""
                SELECT update_izziv(:izziv_id, :selekcija_id, :ime, :opis, :tockovanje, :tedenski_challenge)
            """)
            db.session.execute(query, {
                'izziv_id': izziv_id,
                'selekcija_id': selekcija_id,
                'ime': ime,
                'opis': opis,
                'tockovanje': tockovanje,
                'tedenski_challenge': tedenski_challenge
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Challenge updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## UPDATE IZZIV_IGRALEC CONNECTION
@app.route("/update_izziv_igralec", methods=['POST'])
def update_izziv_igralec():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            izziv_igralec_id = podatki_json.get("izziv_igralec_id")
            trener_id = podatki_json.get("trener_id")
            igralec_id = podatki_json.get("igralec_id")
            izziv_id = podatki_json.get("izziv_id")
            test1 = podatki_json.get("test1")
            test2 = podatki_json.get("test2")

            # Call the update_izziv_igralec function in the database
            query = text("""
                SELECT update_izziv_igralec(:izziv_igralec_id, :trener_id, :igralec_id, :izziv_id, :test1, :test2)
            """)
            db.session.execute(query, {
                'izziv_igralec_id': izziv_igralec_id,
                'trener_id': trener_id,
                'igralec_id': igralec_id,
                'izziv_id': izziv_id,
                'test1': test1,
                'test2': test2
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Challenge participation updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## UPDATE DRUGI_IZZIV
@app.route("/update_drugi_izziv", methods=['POST'])
def update_drugi_izziv():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            drugi_izziv_id = podatki_json.get("drugi_izziv_id")
            ime = podatki_json.get("ime")
            url = podatki_json.get("url")

            # Call the update_drugi_izziv function in the database
            query = text("""
                SELECT update_drugi_izziv(:drugi_izziv_id, :ime, :url)
            """)
            db.session.execute(query, {
                'drugi_izziv_id': drugi_izziv_id,
                'ime': ime,
                'url': url
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Secondary challenge updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## UPDATE DRUGI_IZZIV_IGRALEC CONNECTION
@app.route("/update_drugi_izziv_igralec", methods=['POST'])
def update_drugi_izziv_igralec():
    if request.method == 'POST':
        try:
            # Extract the details from the request data
            podatki_json = request.get_json()
            drugi_izziv_igralec_id = podatki_json.get("drugi_izziv_igralec_id")
            drug_izziv_id = podatki_json.get("drug_izziv_id")
            igralec_id = podatki_json.get("igralec_id")
            trener_id = podatki_json.get("trener_id")
            tocke = podatki_json.get("tocke")
            photo_score = podatki_json.get("photo_score")
            approved = podatki_json.get("approved")

            # Call the update_drugi_izziv_igralec function in the database
            query = text("""
                SELECT update_drugi_izziv_igralec(:drugi_izziv_igralec_id, :drug_izziv_id, :igralec_id, :trener_id, :tocke, :photo_score, :approved)
            """)
            db.session.execute(query, {
                'drugi_izziv_igralec_id': drugi_izziv_igralec_id,
                'drug_izziv_id': drug_izziv_id,
                'igralec_id': igralec_id,
                'trener_id': trener_id,
                'tocke': tocke,
                'photo_score': photo_score,
                'approved': approved
            })

            db.session.commit()

            # Return success response
            return jsonify({'success': True, 'message': 'Secondary challenge participation updated successfully'}), 200

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE KLUB
@app.route("/delete_klub", methods=['POST'])
def delete_klub():
    if request.method == 'POST':
        try:
            # Extract the club ID from the request data
            podatki_json = request.get_json()
            klub_id = podatki_json.get("klub_id")

            # Call the delete_klub function in the database
            query = text("""
                SELECT delete_klub(:klub_id)
            """)
            success = db.session.execute(query, {'klub_id': klub_id}).scalar()

            db.session.commit()

            # Check if the deletion was successful
            if success:
                return jsonify({'success': True, 'message': 'Club deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete club'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE TRENER
@app.route("/delete_trener", methods=['POST'])
def delete_trener():
    if request.method == 'POST':
        try:
            # Extract the coach ID from the request data
            podatki_json = request.get_json()
            trener_id = podatki_json.get("trener_id")

            # Call the delete_trener function in the database
            query = text("""
                SELECT delete_trener(:trener_id)
            """)
            success = db.session.execute(query, {'trener_id': trener_id}).scalar()

            db.session.commit()

            # Check if the deletion was successful
            if success:
                return jsonify({'success': True, 'message': 'Coach deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete coach'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE SELEKCIJA
@app.route("/delete_selekcija", methods=['POST'])
def delete_selekcija():
    if request.method == 'POST':
        try:
            # Extract the selection ID from the request data
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")

            # Call the delete_selekcija function in the database
            query = text("""
                SELECT delete_selekcija(:selekcija_id)
            """)
            success = db.session.execute(query, {'selekcija_id': selekcija_id}).scalar()

            db.session.commit()

            # Check if the deletion was successful
            if success:
                return jsonify({'success': True, 'message': 'Selection deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete selection'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE IGRALEC
@app.route("/delete_igralec", methods=['POST'])
def delete_igralec():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            igralec_id = podatki_json.get("igralec_id")

            query = text("""
                SELECT delete_igralec(:igralec_id)
            """)
            success = db.session.execute(query, {'igralec_id': igralec_id}).scalar()

            db.session.commit()

            if success:
                return jsonify({'success': True, 'message': 'Player deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete player'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE TRENER_SELEKCIJA CONNECTION
@app.route("/delete_trener_selekcija", methods=['POST'])
def delete_trener_selekcija():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            trener_selekcija_id = podatki_json.get("trener_selekcija_id")

            query = text("""
                SELECT delete_trener_selekcija(:trener_selekcija_id)
            """)
            success = db.session.execute(query, {'trener_selekcija_id': trener_selekcija_id}).scalar()

            db.session.commit()

            if success:
                return jsonify({'success': True, 'message': 'Coach-selection association deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete coach-selection association'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE IZZIV
@app.route("/delete_izziv", methods=['POST'])
def delete_izziv():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            izziv_id = podatki_json.get("izziv_id")

            query = text("""
                SELECT delete_izziv(:izziv_id)
            """)
            success = db.session.execute(query, {'izziv_id': izziv_id}).scalar()

            db.session.commit()

            if success:
                return jsonify({'success': True, 'message': 'Challenge deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete challenge'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE IZZIV_IGRALEC CONNECTION
@app.route("/delete_izziv_igralec", methods=['POST'])
def delete_izziv_igralec():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            izziv_igralec_id = podatki_json.get("izziv_igralec_id")

            query = text("""
                SELECT delete_izziv_igralec(:izziv_igralec_id)
            """)
            success = db.session.execute(query, {'izziv_igralec_id': izziv_igralec_id}).scalar()

            db.session.commit()

            if success:
                return jsonify({'success': True, 'message': 'Player challenge entry deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete player challenge entry'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE DRUGI_IZZIV
@app.route("/delete_drugi_izziv", methods=['POST'])
def delete_drugi_izziv():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            drugi_izziv_id = podatki_json.get("drugi_izziv_id")

            query = text("""
                SELECT delete_drugi_izziv(:drugi_izziv_id)
            """)
            success = db.session.execute(query, {'drugi_izziv_id': drugi_izziv_id}).scalar()

            db.session.commit()

            if success:
                return jsonify({'success': True, 'message': 'Secondary challenge deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete secondary challenge'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## DELETE DRUGI_IZZIV_IGRALEC CONNECTION
@app.route("/delete_drugi_izziv_igralec", methods=['POST'])
def delete_drugi_izziv_igralec():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            drugi_izziv_igralec_id = podatki_json.get("drugi_izziv_igralec_id")

            query = text("""
                SELECT delete_drugi_izziv_igralec(:drugi_izziv_igralec_id)
            """)
            success = db.session.execute(query, {'drugi_izziv_igralec_id': drugi_izziv_igralec_id}).scalar()

            db.session.commit()

            if success:
                return jsonify({'success': True, 'message': 'Player secondary challenge entry deleted successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to delete player secondary challenge entry'}), 400

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## GET ALL SELEKCIJE BY KLUB ID
@app.route("/get_all_selekcije_by_klub_id", methods=['POST'])
def get_all_selekcije_by_klub_id():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            klub_id = podatki_json.get("klub_id")

            query = text("""
                SELECT * FROM get_all_selekcije_by_klub_id(:klub_id)
            """)
            result = db.session.execute(query, {'klub_id': klub_id}).fetchall()

            selekcije = [{'id': row.id, 'selekcija': row.selekcija, 'opis': row.opis} for row in result]

            return jsonify({'success': True, 'selekcije': selekcije}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

##GET ALL IGRALCI BY SELEKCIJA ID
@app.route("/get_all_igralci_by_selekcija_id", methods=['POST'])
def get_all_igralci_by_selekcija_id():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")

            query = text("""
                SELECT * FROM get_all_igralci_by_selekcija_id(:selekcija_id)
            """)
            result = db.session.execute(query, {'selekcija_id': selekcija_id}).fetchall()

            igralci = [{'id': row.id, 'ime': row.ime, 'priimek': row.priimek, 'username': row.username, 'tel': row.tel, 'score': row.score} for row in result]

            return jsonify({'success': True, 'igralci': igralci}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## GET METHODES
## GET ALL KLUBI
@app.route("/get_all_klubi", methods=['GET'])
def get_all_klubi():
    if request.method == 'GET':
        try:
            query = text("""
                SELECT * FROM get_all_klubi()
            """)
            result = db.session.execute(query).fetchall()

            klubi = [{'id': row.id, 'ime': row.ime} for row in result]

            return jsonify({'success': True, 'klubi': klubi}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET ALL TRENERJI
@app.route("/get_all_trenerji", methods=['GET'])
def get_all_trenerji():
    if request.method == 'GET':
        try:
            query = text("""
                SELECT * FROM get_all_trenerji()
            """)
            result = db.session.execute(query).fetchall()

            trenerji = [{'id': row.id, 'ime': row.ime, 'priimek': row.priimek, 'gmail': row.gmail, 'tel': row.tel} for row in result]

            return jsonify({'success': True, 'trenerji': trenerji}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET ALL IZZIVI - IDEAS
@app.route("/get_all_izzivi", methods=['GET'])
def get_all_izzivi():
    if request.method == 'GET':
        try:
            query = text("""
                SELECT * FROM get_all_izzivi()
            """)
            result = db.session.execute(query).fetchall()

            izzivi = [{'id': row.id, 'selekcija_id': row.selekcija_id, 'ime': row.ime, 'opis': row.opis, 'točkovanje': row.točkovanje, 'tedenski_challenge': row.tedenski_challenge} for row in result]

            return jsonify({'success': True, 'izzivi': izzivi}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET ALL REGISTRACIJE
@app.route("/get_all_registracije", methods=['GET'])
def get_all_registracije():
    if request.method == 'GET':
        try:
            query = text("""
                SELECT * FROM get_all_registracije()
            """)
            result = db.session.execute(query).fetchall()

            registracije = [{'id': row.id, 'ime': row.ime, 'priimek': row.priimek, 'username': row.username, 'tel': row.tel, 'kraj_kluba': row.kraj_kluba, 'selekcija_id': row.selekcija_id, 'status': row.status} for row in result]

            return jsonify({'success': True, 'registracije': registracije}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET ALL NON APPROVED REGISTRACIJE
@app.route("/get_all_registracije_no", methods=['GET'])
def get_all_registracije_no():
    if request.method == 'GET':
        try:
            query = text("""
                SELECT * FROM get_all_registracije_no()
            """)
            result = db.session.execute(query).fetchall()

            registracije = [{'id': row.id, 'ime': row.ime, 'priimek': row.priimek, 'username': row.username, 'tel': row.tel, 'kraj_kluba': row.kraj_kluba, 'selekcija_id': row.selekcija_id, 'status': row.status} for row in result]

            return jsonify({'success': True, 'registracije': registracije}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## RETURN LEADERBOARD FOR SELECTION
@app.route("/get_leaderboard_by_selekcija", methods=['POST'])
def get_leaderboard_by_selekcija():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")

            query = text("""
                SELECT * FROM get_leaderboard_by_selekcija(:selekcija_id)
            """)
            result = db.session.execute(query, {'selekcija_id': selekcija_id}).fetchall()

            leaderboard = [{'rank': row.rank, 'igralec_id': row.igralec_id, 'ime': row.ime, 'priimek': row.priimek, 'username': row.username, 'total_score': row.total_score} for row in result]

            return jsonify({'success': True, 'leaderboard': leaderboard}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## GET ALL IZZIVI_IGRALCI BY SELECTION
@app.route("/get_all_izzivi_igralci_by_selekcija", methods=['POST'])
def get_all_izzivi_igralci_by_selekcija():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")

            query = text("""
                SELECT * FROM get_all_izzivi_igralci_by_selekcija(:selekcija_id)
            """)
            result = db.session.execute(query, {'selekcija_id': selekcija_id}).fetchall()

            izzivi_igralci = [{'id': row.id, 'trener_id': row.trener_id, 'igralec_id': row.igralec_id, 'izziv_id': row.izziv_id, 'test1': row.test1, 'test2': row.test2, 'score_difference': row.score_difference} for row in result]

            return jsonify({'success': True, 'izzivi_igralci': izzivi_igralci}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## GET ALL DRUGI_IZZIVI BY SELECTION
@app.route("/get_all_drugi_izzivi_by_selekcija", methods=['POST'])
def get_all_drugi_izzivi_by_selekcija():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")

            query = text("""
                SELECT * FROM get_all_drugi_izzivi_by_selekcija(:selekcija_id)
            """)
            result = db.session.execute(query, {'selekcija_id': selekcija_id}).fetchall()

            drugi_izzivi = [{'id': row.id, 'ime': row.ime, 'url': row.url} for row in result]

            return jsonify({'success': True, 'drugi_izzivi': drugi_izzivi}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## GET ALL DRUGI_IZZIVI_IGRALCI BY SELECTION
@app.route("/get_all_drugi_izzivi_igralci_by_selekcija", methods=['POST'])
def get_all_drugi_izzivi_igralci_by_selekcija():
    if request.method == 'POST':
        try:
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")

            query = text("""
                SELECT * FROM get_all_drugi_izzivi_igralci_by_selekcija(:selekcija_id)
            """)
            result = db.session.execute(query, {'selekcija_id': selekcija_id}).fetchall()

            drugi_izzivi_igralci = [
                {
                    'id': row.id, 
                    'drug_izziv_id': row.drug_izziv_id, 
                    'igralec_id': row.igralec_id, 
                    'trener_id': row.trener_id, 
                    'tocke': row.tocke, 
                    'photo_score': row.photo_score, 
                    'approved': row.approved
                } 
                for row in result
            ]

            return jsonify({'success': True, 'drugi_izzivi_igralci': drugi_izzivi_igralci}), 200

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## GET TRENER BY ID
@app.route("/get_trener_by_id", methods=['POST'])
def get_trener_by_id():
    if request.method == 'POST':
        try:
            # Extract the trener_id from the JSON request
            podatki_json = request.get_json()
            trener_id = podatki_json.get("trener_id")

            # Call the SQL function
            query = text("""
                SELECT * FROM get_trener_by_id(:trener_id)
            """)
            result = db.session.execute(query, {'trener_id': trener_id}).fetchone()

            if result:
                trener = {
                    'trenerji_id': result.trenerji_id,
                    'ime': result.ime,
                    'priimek': result.priimek,
                    'gmail': result.gmail,
                    'tel': result.tel
                }
                return jsonify({'success': True, 'trener': trener}), 200
            else:
                return jsonify({'success': False, 'message': 'Trener not found'}), 404

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET IGRALEC BY ID
@app.route("/get_igralec_by_id", methods=['POST'])
def get_igralec_by_id():
    if request.method == 'POST':
        try:
            # Extract the igralec_id from the JSON request
            podatki_json = request.get_json()
            igralec_id = podatki_json.get("igralec_id")

            # Call the SQL function
            query = text("""
                SELECT * FROM get_igralec_by_id(:igralec_id)
            """)
            result = db.session.execute(query, {'igralec_id': igralec_id}).fetchone()

            if result:
                igralec = {
                    'igralci_id': result.igralci_id,
                    'selekcija_id': result.selekcija_id,
                    'ime': result.ime,
                    'priimek': result.priimek,
                    'username': result.username,
                    'tel': result.tel,
                    'score': result.score
                }
                return jsonify({'success': True, 'igralec': igralec}), 200
            else:
                return jsonify({'success': False, 'message': 'Igralec not found'}), 404

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET SELEKCIJA BY ID
@app.route("/get_selekcija_by_id", methods=['POST'])
def get_selekcija_by_id():
    if request.method == 'POST':
        try:
            # Extract the selekcija_id from the JSON request
            podatki_json = request.get_json()
            selekcija_id = podatki_json.get("selekcija_id")

            # Call the SQL function
            query = text("""
                SELECT * FROM get_selekcija_by_id(:selekcija_id)
            """)
            result = db.session.execute(query, {'selekcija_id': selekcija_id}).fetchone()

            if result:
                selekcija = {
                    'selekcije_id': result.selekcije_id,
                    'klub_id': result.klub_id,
                    'selekcija': result.selekcija,
                    'opis': result.opis
                }
                return jsonify({'success': True, 'selekcija': selekcija}), 200
            else:
                return jsonify({'success': False, 'message': 'Selekcija not found'}), 404

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET KLUB BY ID
@app.route("/get_klub_by_id", methods=['POST'])
def get_klub_by_id():
    if request.method == 'POST':
        try:
            # Extract the klub_id from the JSON request
            podatki_json = request.get_json()
            klub_id = podatki_json.get("klub_id")

            # Call the SQL function
            query = text("""
                SELECT * FROM get_klub_by_id(:klub_id)
            """)
            result = db.session.execute(query, {'klub_id': klub_id}).fetchone()

            if result:
                klub = {
                    'klubi_id': result.klubi_id,
                    'ime': result.ime
                }
                return jsonify({'success': True, 'klub': klub}), 200
            else:
                return jsonify({'success': False, 'message': 'Klub not found'}), 404

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET IZZIV BY ID
@app.route("/get_izziv_by_id", methods=['POST'])
def get_izziv_by_id():
    if request.method == 'POST':
        try:
            # Extract the izziv_id from the JSON request
            podatki_json = request.get_json()
            izziv_id = podatki_json.get("izziv_id")

            # Call the SQL function
            query = text("""
                SELECT * FROM get_izziv_by_id(:izziv_id)
            """)
            result = db.session.execute(query, {'izziv_id': izziv_id}).fetchone()

            if result:
                izziv = {
                    'izzivi_id': result.izzivi_id,
                    'selekcija_id': result.selekcija_id,
                    'ime': result.ime,
                    'opis': result.opis,
                    'tockovanje': result.tockovanje,
                    'tedenski_challenge': result.tedenski_challenge
                }
                return jsonify({'success': True, 'izziv': izziv}), 200
            else:
                return jsonify({'success': False, 'message': 'Izziv not found'}), 404

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## GET DRUGI_IZZIV BY ID
@app.route("/get_drugi_izziv_by_id", methods=['POST'])
def get_drugi_izziv_by_id():
    if request.method == 'POST':
        try:
            # Extract the drugi_izziv_id from the JSON request
            podatki_json = request.get_json()
            drugi_izziv_id = podatki_json.get("drugi_izziv_id")

            # Call the SQL function
            query = text("""
                SELECT * FROM get_drugi_izziv_by_id(:drugi_izziv_id)
            """)
            result = db.session.execute(query, {'drugi_izziv_id': drugi_izziv_id}).fetchone()

            if result:
                drugi_izziv = {
                    'drugi_izzivi_id': result.drugi_izzivi_id,
                    'ime': result.ime,
                    'url': result.url
                }
                return jsonify({'success': True, 'drugi_izziv': drugi_izziv}), 200
            else:
                return jsonify({'success': False, 'message': 'Drugi Izziv not found'}), 404

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "POST method not allowed"}), 405

## LOGIN TRENERJI
@app.route("/login_trenerji", methods=['POST'])
def login_trenerji():
    if request.method == 'POST':
        try:
            # Extract the email and password from the JSON request
            podatki_json = request.get_json()
            email = podatki_json.get("email")
            password = podatki_json.get("password")

            # Hash the password
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # Call the SQL function
            query = text("""
                SELECT login_trenerji(:email, :hashed_password)
            """)
            result = db.session.execute(query, {'email': email, 'hashed_password': hashed_password}).scalar()

            if result:
                return jsonify({'success': True, 'message': 'Login successful'}), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405

## LOGIN IGRALCI
@app.route("/login_igralci", methods=['POST'])
def login_igralci():
    if request.method == 'POST':
        try:
            # Extract the username and password from the JSON request
            podatki_json = request.get_json()
            username = podatki_json.get("username")
            password = podatki_json.get("password")

            # Hash the password
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # Call the SQL function
            query = text("""
                SELECT login_igralci(:username, :hashed_password)
            """)
            result = db.session.execute(query, {'username': username, 'hashed_password': hashed_password}).scalar()

            if result:
                return jsonify({'success': True, 'message': 'Login successful'}), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'error': "GET method not allowed"}), 405



if __name__ == '__main__':
    app.run(debug=True)