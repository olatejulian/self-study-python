import sys

from automaton.apps.rpc.example import handler
from automaton.modules.rpc import RpcServer


def main():
    app = RpcServer("127.0.0.1", 8088)

    app.register_handler(handler.MessageHandlerClass())

    app.register_handler(
        handler.message_handler_function, name="message_handler_function"
    )

    app.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
