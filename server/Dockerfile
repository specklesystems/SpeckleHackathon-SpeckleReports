FROM python:3.8.12-bullseye as builder
ENV VIRTUAL_ENV=/opt/venv
RUN pip install --no-cache-dir poetry virtualenv
RUN virtualenv ${VIRTUAL_ENV} 
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root

COPY ./src /src
RUN poetry build -f wheel

RUN ls dist -a 
RUN pip install ./dist/*


FROM python:3.8.12-slim-bullseye
ENV VIRTUAL_ENV=/opt/venv

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY ./app /app

# if  running in kubernetes, or other orchestration env, uvicorn is good enough
# CMD ["uvicorn", "app.main:app"]

CMD ["gunicorn", "-c", "app/gunicorn_conf.py", "-k", "uvicorn.workers.UvicornWorker", "app.main:app" ]