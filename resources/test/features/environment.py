from resources.lib.util.di import Container


def before_scenario(context, scenario):
    context.dependencyInjector = Container()
