FROM python:3.7
WORKDIR /app

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN pip install poetry
COPY poetry.lock poetry.toml pyproject.toml ./
RUN mkdir basement_closet; touch basement_closet/__init__.py
RUN poetry install --no-dev
COPY ./basement_closet ./basement_closet

ENTRYPOINT ["/bin/sh", "-c", "/wait && poetry run uvicorn basement_closet:app \"$@\"", "--"]
CMD ["--port", "8080"]
