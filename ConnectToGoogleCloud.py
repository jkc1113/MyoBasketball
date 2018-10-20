# Imports the Google Cloud client library
from google.cloud import datastore
from google.oauth2 import service_account
from SnapshotDB import Snapshot

import jsonpickle
import json
import myo

class DBConnection:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
        './GoogleCloudStuff/MyoBasketball-6daa0c614684.json')
        # Instantiates a client
        self.datastore_client = datastore.Client(credentials=credentials)

    def storeShot(self, list, name):
        # The kind for the new entity
        kind = 'Shot'

        # The Cloud Datastore key for the new entity
        shot_key = self.datastore_client.key(kind)

        # Prepares the new entity
        shot = datastore.Entity(key=shot_key)
        shot['data'] = jsonpickle.encode(list)
        shot['name'] = name

        # Saves the entity
        self.datastore_client.put(shot)

    def getShotsByUser(self, name):
        query = self.datastore_client.query(kind="Shot")
        query.add_filter('name','=',name)
        quer_iter = query.fetch()
        shots = []
        for entity in quer_iter:
            shots.append(jsonpickle.decode(entity['data']))
        return shots
