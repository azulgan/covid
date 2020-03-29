# /bin/bash
# this program has been created to follow the evolution of the covid19 desease.
# It has been build by Alan Guegan and is totally freely distribuable and modifiable
# the source of data is https://pomber.github.io/covid19/timeseries.json thanks to its autor(s)

dir=`dirname $0`

if [ -f $dir/settings.sh ]; then
  . $dir/settings.sh
fi

function checkOrDownload() {
   if [ -z "$(find $2 -mmin -$3)" ]; then
        curl $1 > $2;
   else
        echo $2 recent enough;
   fi
}
checkOrDownload https://pomber.github.io/covid19/timeseries.json timeseries.json 120
checkOrDownload https://raw.githubusercontent.com/mledoze/countries/master/countries.json countries.json 1440
checkOrDownload https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json country-by-population.json 1440

python import.py
