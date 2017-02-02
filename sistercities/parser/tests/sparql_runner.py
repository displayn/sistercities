import json

with open('query.json') as data_file:
    data = json.load(data_file)

root_cities = []
for rows in data:
    root_cities.append(rows['item'])
# remove duplicates
root_cities = list(set(root_cities))
print(len(root_cities))
