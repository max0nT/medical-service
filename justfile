list:
    @just --list

copy-local-settings:
    cp frontend/.env.local.template frontend/.env
    cp config/.env.local.template config/.env
venv:
    if [ test -d ".venv" ]; then rm -rf .venv; fi;
    uv venv --python 3.12 && source .venv/bin/activate && poetry install
frontend:
    (cd frontend && npx expo start)
go-lint:
    (cd notifications && golangci-lint run)
notifications:
    (cd notifications && go run cmd/main.go)
