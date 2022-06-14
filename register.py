#!/usr/bin/env python
from google.cloud import firestore
import faker

num = 500

def add_from_dict(data:dict):
    db = firestore.Client()
    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection('authors').document().set(data)

def write_data_batch(data: list):
    db = firestore.Client()
    batch = db.batch()

    for d in data:
        doc_ref = db.collection('authors').document()
        batch.set(doc_ref, d)

    batch.commit()


if __name__ == '__main__':
    fake = faker.Faker(['ja_JP'])

    data = []
    for v in range(1,num):
        d = fake.profile()
        del d['birthdate']
        del d['current_location']
        data.append(d)
        print(d)

    write_data_batch(data)
    print()
    print(f"{num} records were writed to Firestore.")
