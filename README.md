# Medical mobile platform

## Short description

A mobile app to provide functions such as:

- Make record to a doctor's session

## Local installation: backend app

In order setup and run backend app you need to have next tools on your machine:

- [uv](https://github.com/astral-sh/uv)
- [poetry](https://github.com/python-poetry/poetry)
- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
- [just](https://github.com/casey/just)

Then install virtual environment

```bash
just setup-deps
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
```bash
just email-run
```

## Stack

FE: react native

BE: FastAPI
