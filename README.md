# Alinea API

Alinea API is a Django application that utilizes Django Channels for real-time features. This guide will help you set up the project locally.

## Prerequisites
- Python 3.6+
- Redis server
- Setup Instructions
### 1. Create a Virtual Environment
It's recommended to use a virtual environment to manage your project's dependencies.

```bash
python3 -m venv venv
```
### 2. Activate the Virtual Environment
On macOS and Linux:

```bash
source venv/bin/activate
```
### 3. Install Dependencies
Install the required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Run Migrations
Make migrations and migrate the database schema:

```bash

python manage.py makemigrations
python manage.py migrate
```
### 5. Create a Superuser
Create an admin user to access the Django admin interface:

```bash
python manage.py createsuperuser
```
Follow the prompts to set up the superuser credentials.

### 6. Start Redis Service
Redis is required for Django Channels to function properly.

Install Redis (macOS)
If you're on macOS, you can install Redis via Homebrew:

```bash
brew install redis
```
### Start Redis Service


```bash
brew services start redis
```
### 7. Start the Server
Start the Daphne server to run the application:

```bash
daphne -p 8000 alinea.asgi:application
```
### 8. Set Up Initial Data
Access the Admin Interface
Log in using the superuser credentials you created earlier.:
http://127.0.0.1:8000/admin/

### Create a User and an Entity
Create a User:

In the admin interface, go to Users and add a new user if necessary.
Create an Entity:

Go to Entities and create a new entity with the desired details.
### 9. Test the Application
Entity Dashboard
Navigate to the entity dashboard page to test the application from the entity's perspective.

### Entity (doctor) Dashboard
Navigate to the user dashboard page to test the application from the user's perspective.
URL:
http://127.0.0.1:8000/entity_dashboard/


### User (patient) Dashboard
http://127.0.0.1:8000/user_dashboard/
Additional Information
API Documentation:

If you have integrated Swagger or another API documentation tool, you can access it at:

http://127.0.0.1:8000/swagger/
Stopping Redis Service:
