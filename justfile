setup-deps:
    if [ test -d ".venv" ]; then rm -rf .venv; fi;
    uv venv --python 3.12 && source .venv/bin/activate && poetry install
email-run:
    python email_notifications/app.py
