import invoke


@invoke.task
def run_hooks(
    context: invoke.context.Context,
    all_repo: bool = False,
) -> None:
    """Run pre commit hook by using prek."""
    all_files_flag = " --all-files" if all_repo else ""
    context.run(f"prek run {all_files_flag}")
