# this program has been created to follow the evolution of the covid19 desease.
# It has been build by Alan Guegan and is totally freely distribuable and modifiable
# the source of data is https://pomber.github.io/covid19/timeseries.json thanks to its autor(s)

import requests, json, os
from elasticsearch import Elasticsearch

esPort = os.getenv('ES_PORT')
esHost = os.getenv('ES_HOST')
esScheme = os.getenv('ES_SCHEME')

#res = requests.get('http://localhost:9200')
#print (res.content)
es = Elasticsearch([{'host': esHost, 'port': esPort}])

i = 1

with open('timeseries.json', 'r') as f:
    timeseries = json.load(f)
    
for country in timeseries:
    for subobject in timeseries[country]:
        print(country)
        subobject['country'] = country
        thedate = subobject['date']
        if thedate[6] == '-':
            thedate = thedate[:5] + "0" + thedate[5:]
        if len(thedate) == 9:
            thedate = thedate[:8] + "0" + thedate[8:]
        subobject['date'] = thedate + "T00:00:00.000Z"
        print(subobject)
        es.index(index='covid', ignore=400, doc_type='spread', id=i, body=subobject)
        i = i + 1


