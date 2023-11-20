
### Solution

I've implemented a Spark app using Structured streaming to ingest the tweet steam, clean up the tweets and store it in Mongo db with the additional infor about the COVID cases from worldmeters.info.

The main components of the app are:

- A StreamReader, reads the stream of tweets from the server and cleans the
format according to the project requirements.
- A Scraper, who fetches the latest covid count from
worldometer.info. The scraper is created and injected into the writer
class, who will request the covid counts.
- Writer, single sink to mongo, takes the batch received, aggregates
the tweets into a single "content" list, adds the timestamp and the covid cases count
provided by the scraper and writes the resulting dataframe to Mongo as
a doc.

There's a basic run.py file that serves as the entrypoint for app:
	- Reads the configuration
	- Sets up spark logger and session objects
	- Creates the different app components and defines the workflow for the streaming process.

#### Configuration

* `SPARK_HOME` configured on your machine, pointing to the location of the Spark binaries and jars (in linux systems, something like `/usr/local/spark`.
* Install the [MongoDB connector for Spark](https://www.mongodb.com/docs/spark-connector/current/)
* Install [Pyton Poetry](https://python-poetry.org/docs/#installation)
* Run `make install-environment` from the project root folder. That will take care of installing the rest of the python dependencies using poetry.

#### How to run the application:

The `Makefile` has commands necessary to run the project:

```
make start-mongo
make stream-simulation
make run-local config-file-name=config/example-config.ini

```

This will sequentially start the Mongo db, the stream simultion and the Spark streaming app.
The config-file-name indicates which config file will be used for running the app, `example-config.ini` has been provided by default, with some values to run it locally.

### How to run the tests

To run the unit tests for the application, use

```
make tests tests_path=unit cov_type=unit
```

This will run the pytest commands and produce a coverage report.
