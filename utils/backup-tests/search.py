import sys
from google.cloud import datastore
from datetime import datetime

client = datastore.Client(database=sys.argv[1])

start_date = datetime(1980, 1, 1).isoformat()

query = client.query(kind='authors')
query.add_filter('birthdate', '>=', start_date)

results = list(query.fetch())

for entity in results:
    print(f"Name: {entity['name']}, Birthdate: {entity['birthdate']}")

print(f"Total entities found: {len(results)}")

