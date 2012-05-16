#! /bin/bash

if [ $# -ne 3 ]; then
	helpme;
fi

function r {
  echo "";
  echo "Uzycie:"
  echo "[sciezkaDoPlikuZdanymi] [nazwaBazy]  [host:port]"
  echo "";
  exit 1
}

source=$1;
dbName=$2;
host=$3;

curl -X DELETE $host/$dbName #usuwamy poprzednia
curl -X PUT $host/$dbName #tworzymy baze
while read line 
do
	curl -d $line -X POST -H "Content-Type: application/json" $host/$dbName #kopiowanie danych
done < $source;

exit 0




