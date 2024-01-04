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
    "measurementId": "G-FRRFLZ6T17"
}
firebase = pyrebase.initialize_app(config)
auth_token = firebase.auth()
database = firebase.database()