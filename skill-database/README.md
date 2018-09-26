## Bitcointalk PostgreSQL
This repository manages a PostgreSQL instance used by `Bitcointalk` for storing data and making computations. 

This database holds data from the BitcoinTalk forum, and is used in our Word2Vec model trainings.


### Usage
This image is better used in production via a `docker-compose.yml` file. The instructions provided in the `Makefile` for development purposes. The following command should work:

```
$ make
```

You will need to have [Docker](https://docker.com) installed in order for the command above to work. If it all goes well, one can evaluate if the database is running via:

```
$ docker ps
ONTAINER ID        IMAGE               COMMAND                  ...
e349008ceaee       skill-bitcointalk-insights-database:v0.0.1        "/usr/local/bin/sk..."   ...
```