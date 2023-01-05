FROM tiangolo/uvicorn-gunicorn:python3.9

COPY . /code

WORKDIR /code

RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && export PATH=$PATH:$HOME/.local/bin \
    && poetry config virtualenvs.create false \
    && poetry install

ENV TZ=America/Sao_Paulo

ENTRYPOINT ["bash", "run.sh"]