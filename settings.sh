if [ -z "$ES" ]; then
  export ES_HOST=localhost
  export ES_PORT=9200
  export ES_SCHEME=http
  export ES=${ES_SCHEME}://${ES_HOST}:${ES_PORT}
fi