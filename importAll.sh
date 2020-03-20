# /bin/bash
# this program has been created to follow the evolution of the covid19 desease.
# It has been build by Alan Guegan and is totally freely distribuable and modifiable
# the source of data is https://pomber.github.io/covid19/timeseries.json thanks to its autor(s)

dir=`dirname $0`

if [ -f $dir/settings.sh ]; then
  . $dir/settings.sh
fi

curl https://pomber.github.io/covid19/timeseries.json > timeseries.json

curl -XDELETE $ES/covid

python import.py
