FROM apache/airflow:2.7.1-python3.10


ARG PROJECT_DIR="/opt/airflow/YoutubeDataCollector/"
ENV PYTHONPATH="$PYTHONPATH:$PROJECT_DIR"

WORKDIR YoutubeDataCollector

RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml $PROJECT_DIR

COPY ./src/helpers $PROJECT_DIR
COPY ./src/dags $PROJECT_DIR
COPY ./src/logs $PROJECT_DIR
COPY ./src/plugins $PROJECT_DIR
COPY ./src/config $PROJECT_DIR

RUN poetry install --no-root

EXPOSE 8080 5555 5432
