# this program has been created to follow the evolution of the covid19 desease.
# It has been build by Alan Guegan and is totally freely distribuable and modifiable
# the source of data is https://pomber.github.io/covid19/timeseries.json thanks to its autor(s)

import requests, json, os
from elasticsearch import Elasticsearch, helpers
import ssl
from elasticsearch import RequestsHttpConnection
import uuid

esPort = os.getenv('ES_PORT')
esHost = os.getenv('ES_HOST')
esScheme = os.getenv('ES_SCHEME')
esUser = os.getenv('ES_USER')
esPass = os.getenv('ES_PASS')
dryRun = os.getenv('dryrun')
#esProxy = os.getenv('ES_PROXY')

#proxies = {"http": esProxy, "https": esProxy}

#class MyConnection(RequestsHttpConnection):
#    def __init__(self, *args, **kwargs):
#        proxies = {"http": esProxy, "https": esProxy}
#        super(MyConnection, self).__init__(*args, **kwargs)
#        self.session.proxies = proxies

#res = requests.get(esScheme + '://' + esHost + ":" + esPort)
#res = requests.get(os.getenv('ES'), proxies=proxies)
#print (res.content)
es = Elasticsearch([{'host': esHost, 'port': esPort}], http_auth=(esUser, esPass), use_ssl=(esScheme=='https')
#                   connection_class = MyConnection, verify_certs=False
)                   # ca_certs=os.getenv('ES_CA_FILE'),


if (dryRun != 'yes'):
    resp=es.indices.delete(index = 'covid')
    print(resp)
    resp=es.indices.create(index = 'covid')
    print(resp)
    resp=es.indices.put_mapping(index='covid', # doc_type='_doc',
                           body={
                                   #"_doc": {
                                       "properties": {
                                           "location": {
                                               "type": "geo_point"
                                           } ,
                                           "date": { "type": "date" },
                                           "confirmed": { "type": "integer" },
                                           "recovered": { "type": "integer" },
                                           "active": { "type": "integer" },
                                           "deaths": { "type": "integer" },
                                           "ratioconfirmed": { "type": "float" },
#                                           "recovered": { "type": "float" },
                                           "ratioactive": { "type": "float" },
                                           "ratiodeaths": { "type": "float" },
                                           "percrecovered": { "type": "float" },
                                           "percdeaths": { "type": "float" },
                                           "country": { "type": "keyword" },
                                           "code": { "type": "keyword" },
                                       }
                                  # }
                                })
    print(resp)

with open('countries.json', 'r') as fc:
    countries_raw = json.load(fc)

countries = dict()

for countryid in countries_raw:
    name=countryid['name']['common']
    code=countryid['cca2']
    pos=countryid['latlng']
    formattedPos='{0:.8f},{1:.8f}'.format(pos[0],pos[1])
    countries[name]={'pos': formattedPos, 'code': code}
    #country = countries_raw[countryid]
    print (name)
    print (countries[name])

with open('countriesMapping.json', 'r') as cm:
    countriesMappings = json.load(cm)

for countriesMapping in countriesMappings:
    countries[countriesMapping['name']]=countries[countriesMapping['alias']]

with open('country-by-population.json', 'r') as cp:
    countriesPop = json.load(cp)

for countryPop in countriesPop:
    curName=countryPop['country']
    country=countries.get(curName)
    if (country == None):
        country={}
    country['pop']=countryPop['population']
    countries[curName]=country

with open('timeseries.json', 'r') as f:
    timeseries = json.load(f)

def parse(val): 
    if val == None: return 0
    return int(val)

def normalizeDate(thedate):
    if thedate[6] == '-':
        thedate = thedate[:5] + "0" + thedate[5:]
    if len(thedate) == 9:
        thedate = thedate[:8] + "0" + thedate[8:]
    return thedate

actions = []

i = 1
for country in timeseries:
    for subobject in timeseries[country]:
        subobject['country'] = country
        subobject['date'] = normalizeDate(subobject['date']) + "T00:00:00.000Z"
        confirmed=parse(subobject['confirmed'])
        subobject['location']=countries[country]['pos']
        subobject['code']=countries[country]['code']
        deaths=parse(subobject['deaths'])
        recovered=parse(subobject['recovered'])
        active=confirmed-recovered-deaths
        subobject['active']=active
        subobject['percrecovered']=0 if confirmed == 0 else (recovered * 100.0 / confirmed)
        subobject['percdeaths']=0 if confirmed == 0 else (deaths * 100.0 / confirmed)
        pop=countries[country].get('pop')
        if (pop != None):
            subobject['pop']=pop
            subobject['ratioactive']=parse(subobject['active']) * 1000000.0 /parse(pop)
            subobject['ratioconfirmed']=parse(subobject['confirmed']) * 1000000.0 /parse(pop)
            subobject['ratiodeaths']=parse(subobject['deaths']) * 1000000.0 /parse(pop)
        print(subobject)
        if (dryRun != 'yes'):
            actions.append({"_id" : uuid.uuid4(), # random UUID for _id
                             "_index": "covid",
                            "_type" : "_doc", # document _type
                         "_source": subobject })
        i = i + 1

helpers.bulk(es, actions)
