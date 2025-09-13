# Medical mobile platform

## Short description

A mobile app to provide functions such as:

- Make record to a doctor's session

## Locally installation: backend app

In order setup and run backend app you need to have next tools on your machine:

- uv
- poetry
- docker/docker-compose

Then install virtual environment

```bash
uv venv --python 3.12 && source .venv/bin/activate && poetry install
```

Then create `.env` file in config directory and move in content to there from `.env.template` file

Next step is run app
```bash
inv fastapi.run
```
There are pre-commit hooks and to use it just run:
```bash
inv pre-commit.run-hooks
```
To run test via pytest use next command:
```bash
inv pytest.run
```

## Locally installation: email microservice

You should follow installation guide for backend app before email microservice app

If you've done it, just run
```
python email_notification/app.py
```

## Stack

FE: react native

BE: FastAPI
