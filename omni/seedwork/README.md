# Python Seedwork

Clean arch and design patterns prototypes

class Module(dependencies)

class Bootstrap(module)
    method init_orm
    method init_scheduler

    method message_bus -> MessageBus(dependencies_injected)

Class MessageBus(dependencies)
    method publish

    method handle calls Handler(message, ...)


class Handler(message, usecase, **dependencies)
    method execute()
    method collect_events() -> list[Event]

