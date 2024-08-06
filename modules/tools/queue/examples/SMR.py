'''
script para realizar duas operações em paralelo,
uma lê dados de uma tabela do postgres utilizando um offset e escreve os dados no redis,
enquanto a outra operação lê os dados do redis e escreve no mongodb.
'''
import multiprocessing as mp
import os
import time
import logging
import asyncio
import asyncpg
import aioredis
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

# constants
REDIS_URL = os.getenv('REDIS_URL')
DATABASE_82 = os.getenv('DATABASE_82')
MONGODB_URL = os.getenv('MONGODB_URL')

path = os.path.dirname(__file__)
FILE_NAME = 'application.log'
file_path = os.path.join(path, FILE_NAME)

logging.basicConfig(
    # filemode='a',
    format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(filename=file_path),
        logging.StreamHandler()
    ]
)

def log(
    database: str,
    start_time,
    exception: Exception = None,
    offset: int = None) -> None:
    '''
    Logs exceptions
    '''
    end_time = time.time()

    if offset is None:
        offset_string = ''
    else:
        offset_string = f'\noffset: {offset}'

    if exception is None:
        info = f'\ndb: {database}{offset_string}\nloop time: {end_time - start_time}\nmessage: Success\n'

        logging.info(info)

    else:
        info = f'\ndb: {database}{offset_string}\nloop time: {end_time - start_time}\nerror: {exception}\n'

        logging.exception(info)

def offsets() -> None:
    '''
    Create offsets queue in Redis
    '''
    # create offsets.
    table_count = 136222998
    step = 50000
    start_offset = 0
    end_offset =  table_count // step + 1

    offsets_list = [i * step for i in range(start_offset, end_offset)]

    return offsets_list

async def read_postgres(conn: any, redis: any, offset: int) -> None:
    '''
    Description:
    ------------
    Read data from Postgres, prepare for JSON format and insert into Redis for queueing.
    '''
    start_time = time.time()

    inu_valid_numbers_post_box_sql_query = f'''
        select
            inu_date_update as datetime,
            inu_id_number as number,
            inu_vendor_hi as vendor
        from
            inu_valid_numbers_post_box
        order by
            datetime asc
        offset {offset}
        limit 50000
    '''

    try:
        results = await conn.fetch(inu_valid_numbers_post_box_sql_query)

    except Exception as exception:
        log(
            database='PostgreSQL',
            offset=offset,
            start_time=start_time,
            exception=exception
        )

    else:
        documents = [
            {
                'datetime': row[0],
                'number': row[1],
                'source': {
                    'name': 'MERA',
                    'vendor': row[2]
                },
                'status': 'answered'
            } for row in results
        ]

        try:
            await redis.rpush('offsets', offset)

            await redis.set(offset, documents)

        except Exception as exception:
            log(
                database='Redis',
                offset=offset,
                start_time=start_time,
                exception=exception
            )

        else:
            log(
                database='PostgreSQL+Redis',
                offset=offset,
                start_time=start_time
            )

async def write_mongo(collection: any, redis: any) -> None:
    '''
    Description:
    ------------
    Read documents for Redis queue and insert into MongoDB.
    '''
    start_time = time.time()

    try:
        offset = await redis.lpop('offsets')

    except Exception as exception:
        log(
            database='Redis',
            start_time=start_time,
            exception=exception
    )

    else:
        try:
            documents = await redis.get(offset)

        except Exception as exception:
            log(
                database='Redis+MongoDB',
                offset=offset,
                start_time=start_time,
                exception=exception
            )

        else:
            try:
                await collection.insert_many(documents)

            except Exception as exception:
                try:
                    await redis.lpush('offsets')

                except Exception as exc:
                    log(
                        database='Redis',
                        offset=offset,
                        start_time=start_time,
                        exception=exc
                    )

            else:
                log(
                    database='MongoDB',
                    offset=offset,
                    start_time=start_time
                )

def run_read_postgres_courotines():
    '''
    Description:
    ------------
    '''
    start_time = time.time()

    redis = aioredis.from_url(
        REDIS_URL,
        encoding='utf-8',
        decode_responses=True
    )

    async def read_coroutines():
        '''
        Description:
        ------------
        '''
        conn = await asyncpg.connect(DATABASE_82.replace('postgresql+asyncpg', 'postgresql'))

        coros = [
            read_postgres(
                conn,
                redis,
                offset
            ) for offset in offsets()
        ]

        await asyncio.gather(*coros)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(read_coroutines())

    except Exception as exception:
        log(
            database='PostgreSQL',
            start_time=start_time,
            exception=exception
        )

    else:
        if loop.is_closed():
            try:
                redis.publish('pubsub_channel', 'read_postgres_courotines_done')

            except Exception as exc:
                log(
                    database='Redis',
                    start_time=start_time,
                    exception=exc
                )

    finally:
        loop.close()

def run_write_mongo_loop():
    '''
    Description:
    ------------
    '''
    # FIXME: A lógica dessa função não está muito clara
    # existe alguns problemas
    start_time = time.time()

    client = AsyncIOMotorClient(MONGODB_URL) # async mongo connection
    database = client['ranknumbers']
    collection = database['numbers']

    async def write_mongo_courotine(collection, loop):

        redis = await aioredis.from_url(
            REDIS_URL,
            encoding='utf-8',
            decode_responses=True
        )

        pubsub = redis.pubsub()

        await pubsub.subscribe('pubsub_channel')

        run = True
        while run is True:
            asyncio.ensure_future(write_mongo(collection, redis))

            try:
                message = await pubsub.get_message()

            except Exception as exception:
                log(
                    database='Redis',
                    start_time=start_time,
                    exception=exception
                )

            else:
                if message:
                    if message['data'] == 'read_postgres_courotines_done':
                        loop.stop()
                        run = False

                    log(
                        'Mongo',
                        start_time,
                    )

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        write_mongo_courotine(
            collection,
            loop
        )
    )

if __name__ == '__main__':
    p1 = mp.Process(
        target=run_read_postgres_courotines,
        name='read_from_postgres'
    )
    p2 = mp.Process(
        target=run_write_mongo_loop,
        name='write_to_mongo'
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()
