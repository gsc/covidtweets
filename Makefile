export APP := covidtweets
export TAG := 0.0.1

setup-environment: install-environment install-linter

.PHONY: install-environment
install-environment:
	poetry env use 3.9
	poetry install

.PHONY: info-environment
info-environment:
	poetry env info
	poetry show --tree

.PHONY: update-environment
update-environment:
	poetry update

.PHONY: install-linter
install-linter:
	poetry run pre-commit clean
	poetry run pre-commit install

.PHONY: linter
linter:
	poetry run pre-commit run --all-files

.PHONY: run-spark-shell
run-spark-shell:
	${SPARK_HOME}/bin/pyspark \
	--master "local[*]" \
	--conf "spark.mongodb.read.connection.uri=mongodb://127.0.0.1:27017/test.apples?readPreference=primaryPreferred" \
	--conf "spark.mongodb.write.connection.uri=mongodb://127.0.0.1:27017/test.apples"


.PHONY: run-local
run-local:
	${SPARK_HOME}/bin/spark-submit \
	--master "local[*]" \
	--conf spark.sql.adaptive.logLevel="info" \
	run.py --config-file-name=${config-file-name}  > my.log

.PHONY: stream-simulation
stream-simulation:
	poetry run python twitter_stream_simulation.py


.PHONY: run
run:
	poetry run python run.py --config-file-name=config/example-config.ini

.PHONY: reset-dirs
reset-dirs:
	rm -r output/
	rm -r checkpoint/
	mkdir output/
	mkdir checkpoint/

.PHONY: start-mongo
start-mongo:
	docker run -p 27017:27017 mongo:4.0.0
