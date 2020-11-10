import csv
import datetime
import json
import requests
from operator import itemgetter 


# 1. Find the ten characters who appear in the most Star Wars films

# initialize empty list
all_chars = []
# get first page
results = requests.get("https://swapi.dev/api/people").json()

# for each item, add it to the list of characters
for item in results['results']:
    all_chars.append(item)

# while there is a next page,
while results['next']:
    # load the results from the next page
    results = requests.get(results['next']).json()
    # for each item in the result,
    for item in results['results']:
        # for each item, add it to the list of characters
        all_chars.append(item)

# get the top 10 characters who are in the most films
sorted_by_most_films = sorted(all_chars, key=lambda i: len(i['films']),reverse=True)[:10]

# 2. Sort those ten characters by height in descending order (i.e., tallest first)
sorted_by_height = sorted(sorted_by_most_films, key = lambda i: int(i['height']), reverse=True)

# 3. Produce a CSV with the following columns: name, species, height, appearances
csv_filename = 'output_{}.csv'.format(datetime.datetime.now().timestamp())
with open(csv_filename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name", "species", "height", "appearances"])

    # put the film appearances into one string
    for item in sorted_by_height:
        item['appearances'] = item['films']
        # get the species from the API
        try:
            species = requests.get(item['species'][0]).json()['name']
        except IndexError:
            species = ""
        # add the item to the CSV
        writer.writerow(
            [item['name']] +
            [species] +
            [item['height']] +
            [len(item['appearances'])]
            )

# 4. Send the CSV to httpbin.org
files = {'upload_file': open(csv_filename, 'rb')}

response = requests.post('http://httpbin.org/post', files=files)

# 5. Create automated tests that validate your code

# test that each item is greater than the next
assert sorted_by_height[1]['height'] > sorted_by_height[2]['height']
# test that there are 10 items in the list
assert len(sorted_by_height) == 10
# test that the api is functioning
assert len(results) != 0
