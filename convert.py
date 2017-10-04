import json

#
# example of parsing original Elasticsearch query output
#

# Reading data back
with open("./samples/es2.txt", 'r', encoding='utf-8') as f:

    data = json.load(f, encoding='utf-8')

    for item in data['hits']['hits']:
        print(item['_source']['originalRequestString'])
