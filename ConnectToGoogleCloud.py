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

    def storeMovement(self, list, mov_type):
        # The kind for the new entity
        kind = 'Movement'
        # The Cloud Datastore key for the new entity
        mov_key = self.datastore_client.key(kind)
        # Prepares the new entity
        mov = datastore.Entity(key=mov_key)
        mov_id = mov['ID']
        mov['mov_type'] = mov_type
        self.datastore_client.put(shot)

        sn_num = 0
        kind = "Snapshot"
        for sn in list:
            sn_key = self.datastore_client.key(kind)
            snap = datastore.Entity(key=sn_key)
            snap["index"] = sn_num
            snap["data"] = jsonpickle.encode(sn)
            snap["mov_id"] = mov_id
            self.datastore_client.put(snap)
            sn_num = sn_num + 1


    def getMovements(self):
        query = self.datastore_client.query(kind="Movement")
        quer_iter = query.fetch()
        movs = []
        for entity in quer_iter:
            query = self.datastore_client.query(kind="Snapshot")
            query.addFilter('mov_id','=',entity['key']['ID'])
            sn_iter = query.fetch()
            snaps = []
            for sn in sn_iter:
                snaps.append(jsonpickle.decode(sn['data']))
            movs.append(snaps)
        return movs
