#!/usr/bin/env python
from google.cloud import datastore
import faker
import click

DEFAULT_NUMBER: int = 500

def add_from_dict(data: dict) -> None:
    client = datastore.Client()
    # Add a new entity to the 'authors' kind
    key = client.key('authors')
    entity = datastore.Entity(key=key)
    entity.update(data)
    client.put(entity)

def write_data_batch(project_id: str, database: str, data: list) -> None:
    client = datastore.Client(project=project_id, database=database)
    batch = client.batch()
    batch.begin()

    for d in data:
        key = client.key('authors')
        entity = datastore.Entity(key=key)
        entity.update(d)
        batch.put(entity)

    batch.commit()

@click.command()
@click.option("--number", "-n", default=DEFAULT_NUMBER)
@click.option("--project", "-p", default=None)
@click.option("--database", "-d", default="(default)")
def run(number: int, project: str, database: str) -> None:
    fake = faker.Faker(['ja_JP'])

    data = []
    for t, v in enumerate(range(0, number)):
        d = fake.profile()
        # del d['birthdate']
        d['birthdate'] = d['birthdate'].isoformat()
        # del d['birthdate']
        del d['sex']
        del d['current_location']
        del d['residence']
        data.append(d)
        print(t+1, ":", d['name'], d['username'], d['job'], d['ssn'], d['address'], d['birthdate'])

    write_data_batch(project, database, data)
    print()
    print(f"{number} records were written to Datastore.")


if __name__ == '__main__':
    run()
