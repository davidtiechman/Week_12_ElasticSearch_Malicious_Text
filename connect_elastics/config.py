from os import getenv
HOST = getenv('ELASTICSEARCH_HOST', 'http://localhost:9200')
PORT = getenv('ELASTICSEARCH_PORT', '9200')