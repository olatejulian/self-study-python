import sys
import time
from datetime import datetime

from automaton.modules.rpc import RpcClient


def main():
    app = RpcClient("127.0.0.1", 8088)

    app.connect()

    while True:
        try:
            response = app.message_handler_class(
                f"hello, it is{datetime.now().strftime(" %Y-%m-%d %H:%M:%S")}"
            )

            print("Message Handler Class Response Data:", response.data)

            response = app.message_handler_function(
                f"hello, it is{datetime.now().strftime(" %Y-%m-%d %H:%M:%S")}"
            )

            print("Message Handler Function Response Data:", response.data)

            time.sleep(2)

        except KeyboardInterrupt:
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
