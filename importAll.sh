# /bin/bash
# this program has been created to follow the evolution of the covid19 desease.
# It has been build by Alan Guegan and is totally freely distribuable and modifiable
# the source of data is https://pomber.github.io/covid19/timeseries.json thanks to its autor(s)

dir=`dirname $0`

if [ -f $dir/settings.sh ]; then
  . $dir/settings.sh
fi

function checkOrDownload() {
   if [ -z "$(find $2 -mmin -120)" ]; then
        curl $1 > $2;
   else
        echo $2 recent enough;
   fi
}
checkOrDownload https://pomber.github.io/covid19/timeseries.json timeseries.json
checkOrDownload https://raw.githubusercontent.com/mledoze/countries/master/countries.json countries.json
checkOrDownload https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json country-by-population.json

python import.py
