# Goal
This project it created to show the evolution over time of the propagation of the covid-19

# HowTo

This project is dependant on python, elastic search and kibana
The source of data is https://pomber.github.io/covid19/timeseries.json

- modify settings.sh to match the current ElasticSearch installation.

- run ./importAll.sh to store the data into your local installation

- run kibana, add the index myindex (yes, I could do better)

- import all in kibana
  - Kibana Management
  - Saved objects
  - Import... export.json
