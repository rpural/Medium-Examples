from faker import Faker
import json

fake = Faker()
data = []

for i in range(10):
  data.append({'name': f'{fake.first_name()} {fake.last_name()}', 'birthdate': str(fake.date_of_birth()), 'email': fake.email()})
  
with open('mediumData.json', 'w') as f:
  json.dump(data, f)
  
