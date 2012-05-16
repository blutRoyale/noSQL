## noSQL


Aplikacja zbierajaca dane z Android Marketu i umieszajaca je w bazach danych.

### Crawling


Aby pobrac dane z marketu wykorzystujemy skrypt crawlMarket.py [plik wyjscia] [kategoria ktora sciagamy]
eg. python crawlMarket.py output.txt BUSINESS

Aby skrypt wymaga paczki BeautifulSoup sciagana przez pip'a. Polecam rowniez wykorzystanie virtualenv.

### Import to MongoDB | CouchDB

Wykorzystujemy do tego skrypty bashowe ImportToMongo.sh i ImportToCouchDB.sh

* Uzycie ImportToMongo.sh:   [sciezkaDoPlikuZdanymi] [nazwaBazy] [nazwa kolekcji] [port]
* Uzycie ImportToCouchDB.sh: [sciezkaDoPlikuZdanymi] [nazwaBazy]  [host:port]

### Export z MongoDB do SQLite

Uruchamiamy skrypt MongoToSqlite.sh
Uzycie: [nazwaBazy] [nazwa kolekcji] [port]

Wynik zostanie zapisany do pliku defaultExport.db.
