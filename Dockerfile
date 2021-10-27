FROM python:3.7
WORKDIR /app
RUN pip install poetry
COPY poetry.lock poetry.toml pyproject.toml ./
RUN mkdir basement_closet; touch basement_closet/__init__.py
RUN poetry install
COPY ./basement_closet ./basement_closet

ENTRYPOINT ["/bin/sh", "-c", "poetry run python -m basement_closet \"$@\"", "--"]