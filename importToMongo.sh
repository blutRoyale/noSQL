#! /bin/bash

function helper() {
  echo "";
  echo "Uzycie:"
  echo "[sciezkaDoPlikuZdanymi] [nazwaBazy] [nazwa kolekcji] [port]"
  echo "";
  exit 1
}

if [ $# -ne 4 ]; then
	helper;
fi

source=$1;
db=$2;
collection=$3;
port=$4;

mongoimport --jsonArray -d $db -c $collection --port $port $source
exit 0



