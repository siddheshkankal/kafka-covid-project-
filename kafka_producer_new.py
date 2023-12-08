


# A simple example demonstrating use of JSONSerializer.

import argparse
from msilib.schema import Registry
from uuid import uuid4
from six.moves import input
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
#from confluent_kafka.schema_registry import *
import pandas as pd
from typing import List

FILE_PATH = "D:\kafka_project\covid_19_india.csv"
columns=["Sno","Date","Time","State/UnionTerritory","ConfirmedIndianNational","ConfirmedForeignNational","Cured","Deaths","Confirmed"]

API_KEY = '5HEVJ7QL23INGI5P'
ENDPOINT_SCHEMA_URL  = 'https://psrc-68gz8.us-east-2.aws.confluent.cloud'
API_SECRET_KEY = 'ieEAKOAj2+I2LO1nzCpFCd1h9tbJ7J0PZuD9MUy+Hdkv2uA8/WgXdAkWg29Ky5C7'
BOOTSTRAP_SERVER = 'pkc-ymrq7.us-east-2.aws.confluent.cloud:9092'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MACHENISM = 'PLAIN'
SCHEMA_REGISTRY_API_KEY = 'KZHWWT2PKM7VUEQX'
SCHEMA_REGISTRY_API_SECRET = '17vuu/RKdkIZVofZpcM8E0dyilClhWTS67waEsgCxCGAQtfH7dh02zI6bQnWnUbC' 


def sasl_conf():

    sasl_conf = {'sasl.mechanism': SSL_MACHENISM,
                 # Set to SASL_SSL to enable TLS support.
                #  'security.protocol': 'SASL_PLAINTEXT'}
                'bootstrap.servers':BOOTSTRAP_SERVER,
                'security.protocol': SECURITY_PROTOCOL,
                'sasl.username': API_KEY,
                'sasl.password': API_SECRET_KEY
                }
    return sasl_conf



def schema_config():
    return {'url':ENDPOINT_SCHEMA_URL,
    
    'basic.auth.user.info':f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}"

    }


class Covid:   
    def __init__(self,record:dict):
        for k,v in record.items():
            setattr(self,k,v)
        
        self.record=record
   
    @staticmethod
    def dict_to_covid(data:dict,ctx):
        return Covid(record=data)

    def __str__(self):
        return f"{self.record}"


def get_covid_instance(file_path):
    df=pd.read_csv(file_path)
    df=df.iloc[:,:]
    covids:List[Covid]=[]
    for data in df.values:
        covid=Covid(dict(zip(columns,data)))
        covids.append(covid)
        yield covid

def covid_to_dict(covid:Covid, ctx):
    """
    Returns a dict representation of a User instance for serialization.
    Args:
        user (User): User instance.
        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    Returns:
        dict: Dict populated with user attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    return covid.record


def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def main(topic):

    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

   
    schema_str = schema_registry_client.get_schema(schema_id = 100003).schema_str

    # print(schema_str)
    string_serializer = StringSerializer('utf_8')
    json_serializer = JSONSerializer(schema_str, schema_registry_client, covid_to_dict)
    # print(json_serializer)
    producer = Producer(sasl_conf())
    # print(producer)
    print("Producing user records to topic {}. ^C to exit.".format(topic))
 
    producer.poll(0.0)

    # info --> counter is used to know how many records published to the topic 
    counter = 0
    try:
        for covid in get_covid_instance(file_path=FILE_PATH):
        
            print(covid)
            producer.produce(topic=topic,
                                key=string_serializer(str(uuid4()), covid_to_dict),
                                value=json_serializer(covid, SerializationContext(topic, MessageField.VALUE)),
                                on_delivery=delivery_report)
            counter += 1

            # info --> loop is break when counter is 5 because we want to publish only 5 records as of now
            if counter == 2:
                break

        # info --> printing at the end how many records got published successfully 
        print(f'totoal number of recorded published are : {counter}')

    except KeyboardInterrupt:
        pass
    except ValueError:
        print("Invalid input, discovidding record...")
        pass

    print("\nFlushing records...")
    producer.flush()

main("covid_19_india")