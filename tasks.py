import invoke
import saritasa_invocations

ns = invoke.Collection(
    saritasa_invocations.docker,
    saritasa_invocations.git,
    saritasa_invocations.github_actions,
    saritasa_invocations.pre_commit,
    saritasa_invocations.system,
    saritasa_invocations.fastapi,
    saritasa_invocations.pytest,
    saritasa_invocations.alembic,
)

# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
        "saritasa_invocations": saritasa_invocations.Config(
            pre_commit=saritasa_invocations.PreCommitSettings(
                hooks=(
                    "pre-commit",
                    "pre-push",
                    "commit-msg",
                ),
            ),
            git=saritasa_invocations.GitSettings(
                merge_ff="true",
                pull_ff="only",
            ),
            docker=saritasa_invocations.DockerSettings(
                main_containers=("postgres", "redis"),
            ),
            fastapi=saritasa_invocations.FastAPISettings(
                app="src.app:app",
            ),
            alembic=saritasa_invocations.AlembicSettings(
                migrations_folder="migrations/versions",
            ),
        ),
    },
)
