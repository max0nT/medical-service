list:
    @just --list

setup-deps:
    if [ test -d ".venv" ]; then rm -rf .venv; fi;
    uv venv --python 3.12 && source .venv/bin/activate && poetry install
go-lint:
    (cd notifications && golangci-lint run)
run-notifications:
    (cd notifications && go run cmd/main.go)
