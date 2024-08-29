
from confluent_kafka import Producer

import grpc
import requests
import threading
import io
import pubsub_api_pb2 as pb2
import pubsub_api_pb2_grpc as pb2_grpc
import avro.schema
import avro.io
import time
import certifi
import json
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta

# Semaphore to keep the program running
semaphore = threading.Semaphore(1)
# Store the latest replay ID
latest_replay_id = None

# Salesforce login credentials
username = os.getenv('SALESFORCE_USERNAME')
password = os.getenv('SALESFORCE_PASSWORD')
security_token = os.getenv('SALESFORCE_SECURITY_TOKEN')
login_url = 'https://saas-ruby-9834.my.salesforce.com/services/Soap/u/59.0/'
headers = {'content-type': 'text/xml', 'SOAPAction': 'login'}

# Store session-related data
session_id = None
instance_url = None
tenant_id = '00DQE000003MOUz2AO'



def establish_grpc_channel():
    with open(certifi.where(), 'rb') as f:
        creds = grpc.ssl_channel_credentials(f.read())
    return grpc.secure_channel('api.pubsub.salesforce.com:7443', creds)

def login():
    global session_id, instance_url
    xml = f"""
    <soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
    xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
    xmlns:urn='urn:partner.soap.sforce.com'>
    <soapenv:Body>
    <urn:login>
    <urn:username><![CDATA[{username}]]></urn:username>
    <urn:password><![CDATA[{password}{security_token}]]></urn:password>
    </urn:login>
    </soapenv:Body>
    </soapenv:Envelope>
    """

    response = requests.post(login_url, data=xml, headers=headers, verify=False)

    if response.status_code == 200:
        # Extract session ID and instance URL from the response
        session_id = extract_session_id(response.content)
        instance_url = extract_instance_url(response.content)
        print("Login successful. Session ID and instance URL obtained.")
        return session_id, instance_url
    else:
        print(f"Login failed with status code {response.status_code}")
        raise Exception("Failed to login to Salesforce")

def extract_session_id(response_content):
    # Extract the session ID from the response XML
    from xml.etree import ElementTree as ET
    tree = ET.fromstring(response_content)
    session_id = tree.find(".//{urn:partner.soap.sforce.com}sessionId").text
    return session_id

def extract_instance_url(response_content):
    # Extract the instance URL from the response XML
    from xml.etree import ElementTree as ET
    tree = ET.fromstring(response_content)
    server_url = tree.find(".//{urn:partner.soap.sforce.com}serverUrl").text
    instance_url = server_url.split('/services')[0]
    return instance_url

def fetchReqStream(topic):
    while True:
        semaphore.acquire()
        yield pb2.FetchRequest(
            topic_name=topic,
            replay_preset=pb2.ReplayPreset.LATEST,
            num_requested=1
        )

def decode(schema, payload):
    schema = avro.schema.parse(schema)
    buf = io.BytesIO(payload)
    decoder = avro.io.BinaryDecoder(buf)
    reader = avro.io.DatumReader(schema)
    return reader.read(decoder)

def encode(schema, payload):
    schema = avro.schema.parse(schema)
    buf = io.BytesIO()
    encoder = avro.io.BinaryEncoder(buf)
    writer = avro.io.DatumWriter(schema)
    writer.write(payload, encoder)
    return buf.getvalue()

def kafka_producer():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'salesforce-pubsub-producer',
    }
    return Producer(conf)

def publish_to_kafka(producer, topic, event):
    producer.produce(topic, value=json.dumps(event))
    producer.flush()


def main():
    global session_id, instance_url

    # Attempt to log in and get a session ID
    login()

    # Create the gRPC channel and stub
    channel = establish_grpc_channel()
    stub = pb2_grpc.PubSubStub(channel)



    # Set up the authentication metadata
    authmetadata = (
        ('accesstoken', session_id),
        ('instanceurl', instance_url),
        ('tenantid', tenant_id)
    )

    mysubtopic = "/data/ContactChangeEvent"
    print('Subscribing to ' + mysubtopic)

    producer = kafka_producer()


    try:
        substream = stub.Subscribe(fetchReqStream(mysubtopic), metadata=authmetadata)
        for event in substream:
            if event.events:
                semaphore.release()
                print("Number of events received: ", len(event.events))
                payloadbytes = event.events[0].event.payload
                schemaid = event.events[0].event.schema_id
                schema = stub.GetSchema(
                    pb2.SchemaRequest(schema_id=schemaid),
                    metadata=authmetadata).schema_json
                decoded = decode(schema, payloadbytes)
                print("Got an event!", json.dumps(decoded))
                publish_to_kafka(producer, 'salesforce_contact_events', decoded)
            else:
                print("[", time.strftime('%b %d, %Y %l:%M%p %Z'), "] The subscription is active.")
            latest_replay_id = event.latest_replay_id
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.UNAUTHENTICATED:
            print("Session expired. Re-authenticating...")
            login()
            main()  # Retry after re-authentication
        else:
            print(f"gRPC error: {e.code()} - {e.details()}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
            main()  # Retry

    mypubtopic = '/event/Contact__e'
    schemaid = stub.GetTopic(pb2.TopicRequest(topic_name=mypubtopic), metadata=authmetadata).schema_id
    schema = stub.GetSchema(pb2.SchemaRequest(schema_id=schemaid), metadata=authmetadata).schema_json

if __name__ == "__main__":
    main()



# import grpc
# import requests
# import threading
# import io
# import pubsub_api_pb2 as pb2
# import pubsub_api_pb2_grpc as pb2_grpc
# import avro.schema
# import avro.io
# import time
# import certifi
# import json
#
# # Semaphore to keep the program running
# semaphore = threading.Semaphore(1)
# # Store the latest replay ID
# latest_replay_id = None
#
# # Salesforce login credentials
# username = 'c-elazzi-twwu@force.com'
# password = 'Camillious1'
# security_token = 'ueFGz7JBCOUzreQMiuxvUlusc'
# login_url = 'https://saas-ruby-9834.my.salesforce.com/services/Soap/u/59.0/'
# headers = {'content-type': 'text/xml', 'SOAPAction': 'login'}
#
# # Store session-related data
# session_id = None
# instance_url = None
# tenant_id = '00DQE000003MOUz2AO'
#
# def establish_grpc_channel():
#     with open(certifi.where(), 'rb') as f:
#         creds = grpc.ssl_channel_credentials(f.read())
#     return grpc.secure_channel('api.pubsub.salesforce.com:7443', creds)
#
# def login():
#     global session_id, instance_url
#     xml = f"""
#     <soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
#     xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
#     xmlns:urn='urn:partner.soap.sforce.com'>
#     <soapenv:Body>
#     <urn:login>
#     <urn:username><![CDATA[{username}]]></urn:username>
#     <urn:password><![CDATA[{password}{security_token}]]></urn:password>
#     </urn:login>
#     </soapenv:Body>
#     </soapenv:Envelope>
#     """
#
#     response = requests.post(login_url, data=xml, headers=headers, verify=False)
#
#     if response.status_code == 200:
#         # Extract session ID and instance URL from the response
#         session_id = extract_session_id(response.content)
#         instance_url = extract_instance_url(response.content)
#         print("Login successful. Session ID and instance URL obtained.")
#     else:
#         print(f"Login failed with status code {response.status_code}")
#         raise Exception("Failed to login to Salesforce")
#
# def extract_session_id(response_content):
#     # Extract the session ID from the response XML
#     from xml.etree import ElementTree as ET
#     tree = ET.fromstring(response_content)
#     session_id = tree.find(".//{urn:partner.soap.sforce.com}sessionId").text
#     return session_id
#
# def extract_instance_url(response_content):
#     # Extract the instance URL from the response XML
#     from xml.etree import ElementTree as ET
#     tree = ET.fromstring(response_content)
#     server_url = tree.find(".//{urn:partner.soap.sforce.com}serverUrl").text
#     instance_url = server_url.split('/services')[0]
#     return instance_url
#
# def fetchReqStream(topic):
#     while True:
#         semaphore.acquire()
#         yield pb2.FetchRequest(
#             topic_name=topic,
#             replay_preset=pb2.ReplayPreset.LATEST,
#             num_requested=1
#         )
#
# def decode(schema, payload):
#     schema = avro.schema.parse(schema)
#     buf = io.BytesIO(payload)
#     decoder = avro.io.BinaryDecoder(buf)
#     reader = avro.io.DatumReader(schema)
#     return reader.read(decoder)
#
# def main():
#     global session_id, instance_url
#
#     # Attempt to log in and get a session ID
#     login()
#
#     # Create the gRPC channel and stub
#     channel = establish_grpc_channel()
#     stub = pb2_grpc.PubSubStub(channel)
#
#     # Set up the authentication metadata
#     authmetadata = (
#         ('accesstoken', session_id),
#         ('instanceurl', instance_url),
#         ('tenantid', tenant_id)
#     )
#
#     mysubtopic = "/data/ContactChangeEvent"
#     print('Subscribing to ' + mysubtopic)
#
#     try:
#         substream = stub.Subscribe(fetchReqStream(mysubtopic), metadata=authmetadata)
#         for event in substream:
#             if event.events:
#                 semaphore.release()
#                 print("Number of events received: ", len(event.events))
#                 payloadbytes = event.events[0].event.payload
#                 schemaid = event.events[0].event.schema_id
#                 schema = stub.GetSchema(
#                     pb2.SchemaRequest(schema_id=schemaid),
#                     metadata=authmetadata).schema_json
#                 decoded = decode(schema, payloadbytes)
#                 print("Got an event!", json.dumps(decoded))
#             else:
#                 print("[", time.strftime('%b %d, %Y %l:%M%p %Z'), "] The subscription is active.")
#             latest_replay_id = event.latest_replay_id
#     except grpc.RpcError as e:
#         if e.code() == grpc.StatusCode.UNAUTHENTICATED:
#             print("Session expired. Re-authenticating...")
#             login()
#             main()  # Retry after re-authentication
#         else:
#             print(f"gRPC error: {e.code()} - {e.details()}")
#             print("Retrying in 5 seconds...")
#             time.sleep(5)
#             main()  # Retry
#
# if __name__ == "__main__":
#     main()

