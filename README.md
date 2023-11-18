#### Spark

* `SPARK_HOME` configured on your machine.


### Components

- A StreamReader, reads the stream of tweets from the server and cleans the
format according to the project requirements.
- A Scraper, who fetches the latest covid count from
worldometer.info. The scraper is created and injected into the writer
class, who will request the covid counts.
- Writer, single sink to mongo, takes the batch received, aggregates
the tweets into a single "content" list, adds the timestamp and the covid cases count
provided by the scraper and writes the resulting dataframe to Mongo as
a doc.

#### How to run it:

```
make run-local config-file-name=config/example-config.ini

```


### Run the tests

```
make tests tests_path=unit cov_type=unit
```
