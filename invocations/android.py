import invoke


@invoke.task
def run(context: invoke.context.Context):
    context.run("(cd ui && npm run android)")
