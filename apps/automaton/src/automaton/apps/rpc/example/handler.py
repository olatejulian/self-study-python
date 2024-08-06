def message_handler_function(message: str):
    received_message = f"Received: {message}"

    print(received_message)

    return received_message


class MessageHandlerClass:
    def __call__(self, message: str):
        return message_handler_function(message)
