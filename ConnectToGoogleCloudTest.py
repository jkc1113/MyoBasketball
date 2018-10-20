# Imports the Google Cloud client library
from google.cloud import datastore
import json

# Instantiates a client
datastore_client = datastore.Client()

# The kind for the new entity
kind = 'Task'
# The name/ID for the new entity
name = 'sampletask1'
# The Cloud Datastore key for the new entity
task_key = datastore_client.key(kind, name)

# Prepares the new entity
task = datastore.Entity(key=task_key)
task['description'] = 'Buy milk'
task['timeToComplete'] = 45

# Saves the entity
datastore_client.put(task)

task2 = datastore_client.get(task_key)

print task2

print('Saved {}: {}'.format(task.key.name, task['description']))
