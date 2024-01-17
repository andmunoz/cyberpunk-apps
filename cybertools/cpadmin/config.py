import collections.abc
import collections
collections.MutableMapping = collections.abc.MutableMapping
collections.Mapping = collections.abc.Mapping
import pyrebase

# Firebase Configurations
config = {
    "apiKey": "AIzaSyD3LUVINjIt9XAHvMZyXojbqGv-EXrKeUk",
    "authDomain": "cyberpunk-database.firebaseapp.com",
    "databaseURL": "https://cyberpunk-database.firebaseio.com",
    "projectId": "cyberpunk-database",
    "storageBucket": "cyberpunk-database.appspot.com",
    "messagingSenderId": "492371389033",
    "appId": "1:492371389033:web:03dc0c1000b49c6b5350f8",
    "measurementId": "G-FRRFLZ6T17",
    "token": "",
}

# Data user authentication
email = "andmunoz@gmail.com"
password = ".La441219"

# Pyrebase initialization
def get_database():
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Authenticated user: ", user['email'])
    except Exception as e:
        print("Authtentication Error: ", e)
        
    return firebase.database()
