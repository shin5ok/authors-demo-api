#!/usr/bin/env python
from google.cloud import firestore
import faker
import click

DEFAULT_NUMBER: int = 500

def add_from_dict(data: dict) -> None:
    db = firestore.Client()
    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection('authors').document().set(data)

def write_data_batch(database: str, data: list) -> None:
    db = firestore.Client(database=database)
    batch = db.batch()

    for d in data:
        doc_ref = db.collection('authors').document()
        batch.set(doc_ref, d)

    batch.commit()

@click.command()
@click.option("--number", "-n", default=DEFAULT_NUMBER)
@click.option("--database", "-d", default="(default)")
def run(number: int, database: str) -> None:
    fake = faker.Faker(['ja_JP'])

    data = []
    for t, v in enumerate(range(0, number)):
        d = fake.profile()
        del d['birthdate']
        del d['sex']
        del d['current_location']
        del d['residence']
        data.append(d)
        print(t+1, ":", d['name'], d['username'], d['job'], d['ssn'], d['address'])

    write_data_batch(database, data)
    print()
    print(f"{number} records were writed to Firestore.")


if __name__ == '__main__':
    run()
