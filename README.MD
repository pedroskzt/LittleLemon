# Little Lemon

## Project Overview
Little Lemon is a project designed as an assessment of understading about Django and RESTful APIs. This project is part of the Meta Coursera Capstone.

## Features
- Register a new User
- Token based Authentication
- CRUD for Menu items
- CRUD for Booking tables

## Endpoints
### Authentication endpoints:

- **POST `/auth/users/`**  
    Register a new user to the system
    - Payload example:
      ```
      {
          "username": "John",
          "password": "lemon@321!,
          "email": "john@example.com"
      }
      ```
    - Expected response:
    `HTTP_201_CREATED`
- **POST `/auth/token/login`**  
    Sign In the user and return its access token
    - Payload example:
      ```
      {
          "username": "John",
          "password": "lemon@321!
      }
      ```
      - Expected response:
      ```
      HTTP_200_OK
      {
        "auth_token": <TOKEN>
      }
      ```
- **POST `/auth/token/logout`**  
    Sign Out the user.
    - Payload example:
    `HTTP_204_NO_CONTENT`

### Menu Endpoints:
- **GET `/restaurant/menu/`**  
    Retrieve the list of menu items.
- **POST `/restaurant/menu/`**  
    Create a new menu item.
    - Fields:
      - Title: title<String>
      - Price: price<Decimal(10,2)>
      - Inventory: inventory<Integer>
- **GET `/restaurant/menu/{id}/`**  
    Retrieve details of a specific menu item.
- **PUT `/restaurant/menu/{id}/`**  
    Update a specific menu item.
- **PATCH `/restaurant/menu/{id}/`**  
    Partial update for a specific menu item.
- **DELETE `/restaurant/menu/{id}/`**  
    Delete a specific menu item.

### Booking Endpoints:
- **GET `/restaurant/bookings/`**  
    Retrieve the list of bookings.
- **POST `/restaurant/bookings/`**  
    Create a new booking.
    - Fields:
      - Name: name<String>
      - Number of guests: no_of_guests<Integer>
      - Booking date: bookingDate<DateTime>
- **GET `/restaurant/bookings/{id}/`**  
    Retrieve details of a specific booking.
- **PUT `/restaurant/bookings/{id}/`**  
    Update a specific booking.
- **DELETE `/restaurant/bookings/{id}/`**  
    Delete a specific booking.

## Download
To set up the project locally, follow these steps:
1. Clone the repository:
    ```
    git clone https://github.com/pedroskzt/LittleLemon.git
    ```

## Instalation
1. Create a new python virtual environment:
    ```
    python -m venv .
    ```

2. Activate the virtual environment:
    - Linux/macOS:
        ```
        source .venv/bin/activate
        ```
    - Windows:
        ```
        .\venv\Scripts\activate
        ```
        or
        ```
        .\venv\Scripts\Activate.ps1
        ```

3. Navigate to the project directory:
    ```
    cd littlelemon
    ```

4. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage
To run the project, use the following command:
1. Check and update the MySQL database configurations:
    - Check the settings file under project folder for database configurations and update it if necessary.

2. Run migrations:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

3. Test the app:
    ```
    python manage.py test
    ```

3. Run the server:
    ```
    python manage.py runserver 
    ```
