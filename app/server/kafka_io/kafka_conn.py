from decouple import config
import asyncio
import json
# from confluent_kafka import AIOKafkaProducer
from aiokafka import AIOKafkaProducer

# env variables
KAFKA_TOPIC = config('KAFKA_TOPIC')
KAFKA_BOOTSTRAP_SERVERS = config('KAFKA_BOOTSTRAP_SERVERS')

loop = asyncio.get_event_loop()

aioproducer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, loop=loop)



# async def send_one(value):
#     producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#     # get cluster layout and initial topic/partition leadership information
#     await producer.start()
#     try:
#         value_json = json.dumps(value).encode('utf-8')
#         await producer.send_and_wait(KAFKA_TOPIC, value_json)
#     finally:
#         # wait for all pending messages to be delivered or expire.
#         await producer.stop()
# loop.run_until_complete(send_one())