import time

class AppService:
    def __init__(self, redis_conn):
        self.redis_connection = redis_conn
        self.redis_key_counter = 0

    def timerize(function):
        def timer(self):
            start_function = time.time()

            # function_return = function(*args, **kwargs)

            end_function = time.time()

            function_delta_time = round(end_function - start_function, 2)

            # return function_return, function_delta_time
            return function_delta_time

    @timerize
    @staticmethod
    def calculate_pi(n):
        pi_approximation = 0
        iterator = 0

        while iterator <= n:
            pi_approximation += 4*((-1)**iterator)/(2*iterator+1)
            # pi_approximation += 8 / ( ( 4 * iterator + 1 ) * ( 4 * iterator + 3) )

            iterator += 1

        return pi_approximation

    def save_redis(self, value):
            key_number = self.redis_key_counter
            redis_key = f'app.service.process:calculate_pi:job:{key_number}'

            try:
                self.redis_connection.set(redis_key, value)

            except Exception as exception:
                print(exception)

            else:
                self.redis_key_counter += 1

            finally:
                self.redis_connection.close()
