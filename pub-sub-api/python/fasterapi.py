# pip install fastapi uvicorn confluent-kafka

from confluent_kafka import Producer, Consumer, KafkaException
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List
import threading
import logging
from publish import publish_to_kafka, kafka_producer  # Import functions from publish.py


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka Producer setup
def kafka_producer():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'fastapi-kafka-producer',
    }
    return Producer(conf)

# Kafka Consumer setup
def kafka_consumer():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'fastapi-kafka-consumer',
        'auto.offset.reset': 'earliest'
    }
    return Consumer(conf)

app = FastAPI()
producer = kafka_producer()
consumer = kafka_consumer()

# In-memory database simulation
contacts_db = {}

# Pydantic model for Contact events
class ContactEvent(BaseModel):
    Id: str
    FirstName: str
    LastName: str
    email: str
    phone: str

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Salesforce Contact Events API"}

# Endpoint for creating a new contact
@app.post("/contacts/")
async def create_contact(event: ContactEvent):
    try:
        event_data = event.dict()
        event_data['event_type'] = 'creation'
      #  publish_to_kafka(producer, 'salesforce_contact_events', event_data)  # Call the function from publish.py

        producer.produce('salesforce_contact_events', value=json.dumps(event_data))
        producer.flush()

        # Update in-memory database
        contacts_db[event_data['Id']] = event_data
        logger.info(f"Contact {event_data['Id']} created and added to contacts_db")

        return {"status": "Contact created and event sent to Kafka", "event": event_data}
    except Exception as e:
        logger.error(f"Error creating contact: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating contact: {str(e)}")

# Endpoint for updating an existing contact
@app.put("/contacts/{Id}/")
async def update_contact(Id: str, event: ContactEvent):
    try:
        event_data = event.dict()
        event_data['event_type'] = 'update'

        if event_data['Id'] != Id:
            raise HTTPException(status_code=400, detail="Contact ID in URL and body do not match")
       # publish_to_kafka(producer, 'salesforce_contact_events', event_data)  # Call the function from publish.py

        producer.produce('salesforce_contact_events', value=json.dumps(event_data))
        producer.flush()

        # Update in-memory database
        if Id not in contacts_db:
            raise HTTPException(status_code=404, detail="Contact not found")

        contacts_db[Id] = event_data
        logger.info(f"Contact {Id} updated in contacts_db")

        return {"status": "Contact updated and event sent to Kafka", "event": event_data}
    except Exception as e:
        logger.error(f"Error updating contact: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating contact: {str(e)}")

# Endpoint to get all contacts
@app.get("/contacts/", response_model=List[ContactEvent])
async def get_all_contacts():
    try:
        # Convert in-memory dictionary to list of ContactEvent
        contacts_list = list(contacts_db.values())
        logger.info(f"Retrieved {len(contacts_list)} contacts from contacts_db")
        return contacts_list
    except Exception as e:
        logger.error(f"Error retrieving contacts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving contacts: {str(e)}")

# Endpoint to get a specific contact by ID
@app.get("/contacts/{Id}/", response_model=ContactEvent)
async def get_contact(Id: str):
    try:
        contact = contacts_db.get(Id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        logger.info(f"Retrieved contact {Id} from contacts_db")
        return contact
    except Exception as e:
        logger.error(f"Error retrieving contact: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving contact: {str(e)}")

# Kafka Consumer loop
def consume_kafka_messages():
    consumer.subscribe(['salesforce_contact_events'])
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            logger.error(f"Kafka Error: {msg.error()}")
            continue

        try:
            event_data = json.loads(msg.value().decode('utf-8'))
            Id = event_data.get('Id')

            # Update in-memory database
            if event_data['event_type'] in ['creation', 'update']:
                contacts_db[Id] = event_data
                logger.info(f"Updated contact {Id} in contacts_db")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

# Start Kafka Consumer thread
consumer_thread = threading.Thread(target=consume_kafka_messages, daemon=True)
consumer_thread.start()