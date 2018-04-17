import os

import pyrebase

FIREBASE_API_KEY = 'FIREBASE_API_KEY'
FIREBASE_PROJECT_ID = 'FIREBASE_PROJECT_ID'
FIREBASE_DATABASE_URL = 'FIREBASE_DATABASE_URL'


class Api:

    class Error(Exception):
        pass

    def __init__(self, config: dict):
        if config:
            api_key = config.get('api_key')
            project_id = config.get('project_id')
            database_url = config.get('database_url')
        else:
            api_key = os.environ.get(FIREBASE_API_KEY)
            project_id = os.environ.get(FIREBASE_PROJECT_ID)
            database_url = os.environ.get(FIREBASE_DATABASE_URL)

        if not api_key:
            raise self.Error(
                f'Firebase API key not found. Please set env var `{FIREBASE_API_KEY}`'
            )

        if not project_id:
            raise self.Error(
                f'Firebase project id not found. Please set env var `{FIREBASE_PROJECT_ID}`'
            )

        if not database_url:
            raise self.Error(
                f'Firebase database url not found. Please set env var `{FIREBASE_DATABASE_URL}`'
            )

        self.config = {
            "apiKey": api_key,
            "authDomain": f"{project_id}.firebaseapp.com",
            "databaseURL": database_url,
            "storageBucket": f"{project_id}.appspot.com"
        }

        self.firebase = pyrebase.initialize_app(self.config)

    def save(self, data: dict):
        self.firebase.database().child("data").set(data)

    def load(self) -> dict:
        data = self.firebase.database().child("data").get().val()
        if data is not None:
            return dict(data)

        return {}
