# Local installation

## Required tools

- [uv](https://github.com/astral-sh/uv)
- [poetry](https://github.com/python-poetry/poetry)

- [go 1.25](https://github.com/golang/go)
- [golangci](https://github.com/golangci/golangci-lint)

- [nvm](https://github.com/nvm-sh/nvm)

- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
- [just](https://github.com/casey/just)
- [prek](https://github.com/j178/prek)


## Core backend app

Then install virtual environment

```bash
just setup-deps
```

Then create `.env` file in config directory and move in content to there from `.env.template` file

Next step is run app
```bash
inv fastapi.run
```

## Email notification

To run email notification service, install dependencies

```bash
(cd notifications && go mod download)
```
After that you can run it
```bash
just run-notifications
```

## Android app

Before start, you have to do following steps:

1. Install android sdk and path to it as `ANDROID_HOME` env variable
2. Install node dependencies, note you should use node version 20.19.4 and higher
otherwise you won't able to run app
```bash
(cd ui && npm install)
```
3. To run app need to run. Please remember you don't have to repeat step 1 - 2 when you do it one times
```bash
just android-run
```
