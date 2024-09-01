# API Documentation

This API provides endpoints for managing a sports club system, including managing players (Igralci), coaches (Trenerji), clubs (Klubi), selections (Selekcije), and challenges (Izzivi). Database is on ElephantSQL which will cease to exist in 2025. API is for application testrun and all components including databse will be moved to production if testrun is a success.

## Endpoints

### GET Endpoints

#### 1. Get All Klubi

- **Endpoint:** `/get_all_klubi`
- **Method:** `GET`
- **Description:** Retrieves all clubs.
- **Response:**
  {
    "success": true,
    "klubi": [
      {
        "id": 1,
        "ime": "Klub Name"
      }
    ]
  }

#### 2. Get All Trenerji

- **Endpoint:** `/get_all_trenerji`
- **Method:** `GET`
- **Description:** Retrieves all coaches.
- **Response:**
  {
    "success": true,
    "trenerji": [
      {
        "id": 1,
        "ime": "First Name",
        "priimek": "Last Name",
        "gmail": "email@example.com",
        "tel": "123456789"
      }
    ]
  }

#### 3. Get All Izzivi

- **Endpoint:** `/get_all_izzivi`
- **Method:** `GET`
- **Description:** Retrieves all challenges.
- **Response:**
  {
    "success": true,
    "izzivi": [
      {
        "id": 1,
        "selekcija_id": 1,
        "ime": "Challenge Name",
        "opis": "Description",
        "tockovanje": "Scoring",
        "tedenski_challenge": true
      }
    ]
  }

#### 4. Get All Registracije

- **Endpoint:** `/get_all_registracije`
- **Method:** `GET`
- **Description:** Retrieves all registrations.
- **Response:**
  {
    "success": true,
    "registracije": [
      {
        "id": 1,
        "ime": "First Name",
        "priimek": "Last Name",
        "username": "username",
        "tel": "123456789",
        "kraj_kluba": "City",
        "selekcija_id": 1,
        "status": "pending"
      }
    ]
  }

#### 5. Get All Non-Approved Registracije

- **Endpoint:** `/get_all_registracije_no`
- **Method:** `GET`
- **Description:** Retrieves all pending registrations.
- **Response:**
  {
    "success": true,
    "registracije": [
      {
        "id": 1,
        "ime": "First Name",
        "priimek": "Last Name",
        "username": "username",
        "tel": "123456789",
        "kraj_kluba": "City",
        "selekcija_id": 1,
        "status": "pending"
      }
    ]
  }

### POST Endpoints

#### 1. Register User

- **Endpoint:** `/register`
- **Method:** `POST`
- **Description:** Registers a new user (either a coach or a player).
- **Request:**
  {
    "FirstName": "John",
    "LastName": "Doe",
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "password123",
    "tel": "123456789",
    "kraj_kluba": "City",
    "selekcija_id": 1,
    "tip": "trener"
  }
- **Response:**
  {
    "success": true,
    "registracija_id": 1
  }

#### 2. Approve Registration

- **Endpoint:** `/approve_registration`
- **Method:** `POST`
- **Description:** Approves a pending registration.
- **Request:**
  {
    "registracija_id": 1
  }
- **Response:**
  {
    "success": true,
    "message": "Registration approved successfully"
  }
  OR
  {
    "success": false,
    "message": "Approval failed or registration already processed"
  }

#### 3. Create Klub

- **Endpoint:** `/create_klub`
- **Method:** `POST`
- **Description:** Creates a new club.
- **Request:**
  {
    "klub_ime": "Nogometni Klub"
  }
- **Response:**
  {
    "success": true,
    "klub_id": 1
  }

#### 4. Create Selekcija

- **Endpoint:** `/create_selekcija`
- **Method:** `POST`
- **Description:** Creates a new selection.
- **Request:**
  {
    "klub_id": 1,
    "selekcija_ime": "U15",
    "opis": "Youth team"
  }
- **Response:**
  {
    "success": true,
    "selekcija_id": 1
  }

#### 5. Create Trener Selekcija

- **Endpoint:** `/create_trener_selekcija`
- **Method:** `POST`
- **Description:** Assigns a coach to a selection.
- **Request:**
  {
    "trener_id": 1,
    "selekcija_id": 1
  }
- **Response:**
  {
    "success": true,
    "trener_selekcija_id": 1
  }

#### 6. Create Izziv

- **Endpoint:** `/create_izziv`
- **Method:** `POST`
- **Description:** Creates a new challenge.
- **Request:**
  {
    "selekcija_id": 1,
    "ime": "Weekly Challenge",
    "opis": "This is a challenge for this week.",
    "tockovanje": "Scoring details",
    "tedenski_challenge": true
  }
- **Response:**
  {
    "success": true,
    "izziv_id": 1
  }

#### 7. Create Izziv Igralec

- **Endpoint:** `/create_izziv_igralec`
- **Method:** `POST`
- **Description:** Assigns a player to a challenge.
- **Request:**
  {
    "trener_id": 1,
    "igralec_id": 1,
    "izziv_id": 1,
    "test1": 5.5
  }
- **Response:**
  {
    "success": true,
    "izziv_igralec_id": 1
  }

#### 8. Create Drugi Izziv

- **Endpoint:** `/create_drugi_izziv`
- **Method:** `POST`
- **Description:** Creates a new additional challenge.
- **Request:**
  {
    "ime": "Extra Challenge",
    "url": "http://example.com/challenge"
  }
- **Response:**
  {
    "success": true,
    "drugi_izziv_id": 1
  }

#### 9. Create Drugi Izziv Igralec

- **Endpoint:** `/create_drugi_izziv_igralec`
- **Method:** `POST`
- **Description:** Assigns a player to an additional challenge.
- **Request:**
  {
    "drug_izziv_id": 1,
    "igralec_id": 1,
    "trener_id": 1
  }
- **Response:**
  {
    "success": true,
    "drugi_izziv_igralec_id": 1
  }

### DELETE Endpoints

#### 1. Delete Klub

- **Endpoint:** `/delete_klub`
- **Method:** `POST`
- **Description:** Deletes a club.
- **Request:**
  {
    "klub_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 2. Delete Trener

- **Endpoint:** `/delete_trener`
- **Method:** `POST`
- **Description:** Deletes a coach.
- **Request:**
  {
    "trener_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 3. Delete Selekcija

- **Endpoint:** `/delete_selekcija`
- **Method:** `POST`
- **Description:** Deletes a selection.
- **Request:**
  {
    "selekcija_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 4. Delete Igralec

- **Endpoint:** `/delete_igralec`
- **Method:** `POST`
- **Description:** Deletes a player.
- **Request:**
  {
    "igralec_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 5. Delete Trener Selekcija

- **Endpoint:** `/delete_trener_selekcija`
- **Method:** `POST`
- **Description:** Deletes a coach's assignment to a selection.
- **Request:**
  {
    "trener_selekcija_id": 1
  }
- **Response:**
    {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 6. Delete Izziv

- **Endpoint:** `/delete_izziv`
- **Method:** `POST`
- **Description:** Deletes a challenge.
- **Request:**
  {
    "izziv_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 7. Delete Izziv Igralec

- **Endpoint:** `/delete_izziv_igralec`
- **Method:** `POST`
- **Description:** Deletes a player's participation in a challenge.
- **Request:**
  {
    "izziv_igralec_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 8. Delete Drugi Izziv

- **Endpoint:** `/delete_drugi_izziv`
- **Method:** `POST`
- **Description:** Deletes an additional challenge.
- **Request:**
  {
    "drugi_izziv_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 9. Delete Drugi Izziv Igralec

- **Endpoint:** `/delete_drugi_izziv_igralec`
- **Method:** `POST`
- **Description:** Deletes a player's participation in an additional challenge.
- **Request:**
  {
    "drugi_izziv_igralec_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

### UPDATE Endpoints

#### 1. Update Klub

- **Endpoint:** `/update_klub`
- **Method:** `POST`
- **Description:** Updates club details.
- **Request:**
  {
    "klub_id": 1,
    "ime": "Updated Klub Name"
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 2. Update Trener

- **Endpoint:** `/update_trener`
- **Method:** `POST`
- **Description:** Updates coach details.
- **Request:**
  {
    "trener_id": 1,
    "ime": "Updated First Name",
    "priimek": "Updated Last Name",
    "gmail": "updated.email@example.com",
    "geslo": "newpassword",
    "tel": "987654321"
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 3. Update Selekcija

- **Endpoint:** `/update_selekcija`
- **Method:** `POST`
- **Description:** Updates selection details.
- **Request:**
  {
    "selekcija_id": 1,
    "klub_id": 1,
    "selekcija": "Updated Selekcija",
    "opis": "Updated description"
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 4. Update Igralec

- **Endpoint:** `/update_igralec`
- **Method:** `POST`
- **Description:** Updates player details.
- **Request:**
  {
    "igralec_id": 1,
    "selekcija_id": 1,
    "ime": "Updated First Name",
    "priimek": "Updated Last Name",
    "username": "updatedusername",
    "geslo": "newpassword",
    "tel": "987654321",
    "score": 90.5
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 5. Update Trener Selekcija

- **Endpoint:** `/update_trener_selekcija`
- **Method:** `POST`
- **Description:** Updates the assignment of a coach to a selection.
- **Request:**
  {
    "trener_selekcija_id": 1,
    "trener_id": 1,
    "selekcija_id": 1
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 6. Update Izziv

- **Endpoint:** `/update_izziv`
- **Method:** `POST`
- **Description:** Updates challenge details.
- **Request:**
  {
    "izziv_id": 1,
    "selekcija_id": 1,
    "ime": "Updated Challenge Name",
    "opis": "Updated description",
    "tockovanje": "Updated scoring",
    "tedenski_challenge": true
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 7. Update Izziv Igralec

- **Endpoint:** `/update_izziv_igralec`
- **Method:** `POST`
- **Description:** Updates a player's performance in a challenge.
- **Request:**
  {
    "izziv_igralec_id": 1,
    "trener_id": 1,
    "igralec_id": 1,
    "izziv_id": 1,
    "test1": 5.5,
    "test2": 6.5
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 8. Update Drugi Izziv

- **Endpoint:** `/update_drugi_izziv`
- **Method:** `POST`
- **Description:** Updates additional challenge details.
- **Request:**
  {
    "drugi_izziv_id": 1,
    "ime": "Updated Challenge Name",
    "url": "http://example.com/updatedchallenge"
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

#### 9. Update Drugi Izziv Igralec

- **Endpoint:** `/update_drugi_izziv_igralec`
- **Method:** `POST`
- **Description:** Updates a player's participation in an additional challenge.
- **Request:**
  {
    "drugi_izziv_igralec_id": 1,
    "drug_izziv_id": 1,
    "igralec_id": 1,
    "trener_id": 1,
    "tocke": 100,
    "photo_score": 5.5,
    "approved": true
  }
- **Response:**
  {
    "success": true
  }
  OR
  {
    "success": false
  }

### RETRIEVE Endpoints

#### 1. Get Trener By ID

- **Endpoint:** `/get_trener_by_id`
- **Method:** `POST`
- **Description:** Retrieves a coach by ID.
- **Request:**
  {
    "trener_id": 1
  }
- **Response:**
  {
    "success": true,
    "trener": {
      "trenerji_id": 1,
      "ime": "First Name",
      "priimek": "Last Name",
      "gmail": "email@example.com",
      "tel": "123456789"
    }
  }
  OR
  {
    "success": false
  }

#### 2. Get Igralec By ID

- **Endpoint:** `/get_igralec_by_id`
- **Method:** `POST`
- **Description:** Retrieves a player by ID.
- **Request:**
  {
    "igralec_id": 1
  }
- **Response:**
  {
    "success": true,
    "igralec": {
      "igralci_id": 1,
      "selekcija_id": 1,
      "ime": "First Name",
      "priimek": "Last Name",
      "username": "username",
      "tel": "123456789",
      "score": 85.5
    }
  }
  OR
  {
    "success": false
  }

#### 3. Get Selekcija By ID

- **Endpoint:** `/get_selekcija_by_id`
- **Method:** `POST`
- **Description:** Retrieves a selection by ID.
- **Request:**
  {
    "selekcija_id": 1
  }
- **Response:**
  {
    "success": true,
    "selekcija": {
      "selekcije_id": 1,
      "klub_id": 1,
      "selekcija": "Selekcija Name",
      "opis": "Description"
    }
  }
  OR
  {
    "success": false
  }

#### 4. Get Klub By ID

- **Endpoint:** `/get_klub_by_id`
- **Method:** `POST`
- **Description:** Retrieves a club by ID.
- **Request:**
  {
    "klub_id": 1
  }
- **Response:**
  {
    "success": true,
    "klub": {
        "klubi_id": 1,
            "ime": "Klub Name"
            }
        }
        OR
        {
            "success": false
        }
        
#### 5. Get Izziv By ID

- **Endpoint:** `/get_izziv_by_id`
- **Method:** `POST`
- **Description:** Retrieves a challenge by ID.
- **Request:**
  {
    "izziv_id": 1
  }
- **Response:**
  {
    "success": true,
    "izziv": {
      "izzivi_id": 1,
      "selekcija_id": 1,
      "ime": "Challenge Name",
      "opis": "Description",
      "tockovanje": "Scoring details",
      "tedenski_challenge": true
    }
  }
  OR
  {
    "success": false
  }

#### 6. Get Drugi Izziv By ID

- **Endpoint:** `/get_drugi_izziv_by_id`
- **Method:** `POST`
- **Description:** Retrieves an additional challenge by ID.
- **Request:**
  {
    "drugi_izziv_id": 1
  }
- **Response:**
  {
    "success": true,
    "drugi_izziv": {
      "drugi_izzivi_id": 1,
      "ime": "Challenge Name",
      "url": "http://example.com/challenge"
    }
  }
  OR
  {
    "success": false
  }

### LOGIN Endpoints

#### 1. Login Trenerji

- **Endpoint:** `/login_trenerji`
- **Method:** `POST`
- **Description:** Authenticates a coach's login.
- **Request:**
  {
    "email": "email@example.com",
    "password": "password123"
  }
- **Response:**
  {
    "success": true,
    "message": "Login successful",
    "trener_id": 1
  }
  OR
  {
    "success": false,
    "message": "Invalid credentials"
  }

#### 2. Login Igralci

- **Endpoint:** `/login_igralci`
- **Method:** `POST`
- **Description:** Authenticates a player's login.
- **Request:**
  {
    "username": "username",
    "password": "password123"
  }
- **Response:**
  {
    "success": true,
    "message": "Login successful",
    "igralec_id": 1
  }
  OR
  {
    "success": false,
    "message": "Invalid credentials"
  }
    
