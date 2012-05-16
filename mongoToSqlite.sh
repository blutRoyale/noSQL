#! /bin/bash

# Eksport danych z mongoDB do MySQL

# Funkcja pokazuje sposob uzycia skrypt
function helpme() {
  echo "";
  echo "Uzycie MongoToSqlite dla MongoDB:"
  echo "[nazwaBazy] [nazwa kolekcji] [port]"
  exit 1
}

# sprawdzanie ilosci parametrow
if [ $# -ne 3 ]; then
	helpme;
fi

# pobieranie zmiennych
outputFile="./export.txt";
dbName=$1
collection=$2
port=$3

mongoexport -d $dbName -c $collection -o $outputFile --port $port

python exportToSqlite.py


