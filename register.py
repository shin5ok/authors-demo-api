#!/usr/bin/env python
from google.cloud import firestore


def add_from_dict(data:dict):
    db = firestore.Client()
    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection('authors').document().set(data)

def update_data_batch(data: list):
    db = firestore.Client()
    batch = db.batch()

    for d in data:
        doc_ref = db.collection('authors').document()
        batch.set(doc_ref, d)

    batch.commit()

import faker

fake=faker.Faker(['ja_JP'])

data = []
for v in range(1,500):
    d=fake.profile()
    del d['birthdate']
    del d['current_location']
    # add_from_dict(d)
    data.append(d)
    print(d)

update_data_batch(data)
