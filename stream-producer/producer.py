import json
import boto3
import uuid
import logging
from twitter import Api
import os

logging.basicConfig(filename="./producer.py.log",
                    level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# get Twitter app credentials from environment variables
CONSUMER_KEY = os.getenv("CONSUMER_KEY", None)
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET", None)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET", None)

# List of users to watch Twitter for mentions of:
USERS = ['@awsformobile']

LANGUAGES = ['en']

api = Api(CONSUMER_KEY,
          CONSUMER_SECRET,
          ACCESS_TOKEN,
          ACCESS_TOKEN_SECRET)

client = boto3.client('kinesis', region_name='us-east-1')


def main():
    try:
        # api.GetStreamFilter returns a generator that yields one Tweet at a time as a JSON dictionary
        for line in api.GetStreamFilter(track=USERS, languages=LANGUAGES):
            # put on Kinesis stream called 'tweets'
            response = client.put_record(
                StreamName='tweets',
                Data=json.dumps(line),
                PartitionKey=str(uuid.uuid4()),
            )
            logging.info("writing to stream with: \n" + str(json.dumps(line)))
            logging.info("Kinesis response: \n" + str(response))
    except Exception as e:
        logging.error("Main function crashed. Error: %s", e)


if __name__ == '__main__':
    main()
