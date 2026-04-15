# Local installation

## Required tools

- [uv](https://github.com/astral-sh/uv)
- [poetry](https://github.com/python-poetry/poetry)

- [go 1.25](https://github.com/golang/go)
- [golangci](https://github.com/golangci/golangci-lint)

- [nvm](https://github.com/nvm-sh/nvm)
- [npx]()

- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
- [just](https://github.com/casey/just)
- [prek](https://github.com/j178/prek)


## Core backend app

Then install virtual environment

```bash
just venv
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
just notifications
```

## Android app

Mobile app locally is available too

1. You should install [expo](https://docs.expo.dev/) on either [Android 16 SDK](https://developer.android.com/about/versions/16/setup-sdk?hl=en)
or you test device
2. Install node version 20.9.4 and higher
```bash
nvm install 20.9.4 && nvm use 20.19.4
```
3. Load all dependencies
```bash
npm install
```
4. When all steps are done, android app is available by running a command
```bash
just frontend
```
