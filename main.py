import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from simple_salesforce import Salesforce
import logging
from typing import Optional, List
from confluent_kafka import Producer, Consumer

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

KAFKA_CONFIG = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'client.id': 'fastapi-client'
}

# Initialize Kafka Producer
producer = Producer(KAFKA_CONFIG)

def kafka_produce(topic: str, message: dict):
    try:
        producer.produce(topic, key=str(message.get('id')), value=str(message))
        producer.flush()
    except Exception as e:
        logging.error(f"Error producing message to Kafka: {e}")
        raise HTTPException(status_code=500, detail="Error producing message to Kafka")
# Function to get Salesforce instance using simple_salesforce
def get_salesforce_instance() -> Salesforce:
    username = os.getenv('SALESFORCE_USERNAME')
    password = os.getenv('SALESFORCE_PASSWORD')
    security_token = os.getenv('SALESFORCE_SECURITY_TOKEN')

    try:
        sf = Salesforce(username=username, password=password, security_token=security_token)
        return sf
    except Exception as e:
        logging.error(f"Error connecting to Salesforce: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to Salesforce")

app = FastAPI()

class CustomerEvent(BaseModel):
    first_name: str
    last_name: str
    email: str

@app.post("/contact")
async def handle_event(event: CustomerEvent):
    sf = get_salesforce_instance()
    try:
        # Create new contact in Salesforce
        new_contact = sf.Contact.create({
            'FirstName': event.first_name,
            'LastName': event.last_name,
            'Email': event.email
        })
        # Send event to Kafka
        kafka_produce('contact-created-topic', {
            'id': new_contact['id'],
            'first_name': event.first_name,
            'last_name': event.last_name,
            'email': event.email
        })
        return {"status": "success", "contact_id": new_contact['id']}
    except Exception as e:
        logging.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail="Error creating contact")

@app.put("/contact/{contact_id}")
async def update_contact(contact_id: str, event: CustomerEvent):
    sf = get_salesforce_instance()
    try:
        # Update existing contact in Salesforce
        updated_contact = sf.Contact.update(contact_id, {
            'FirstName': event.first_name,
            'LastName': event.last_name,
            'Email': event.email
        })
        return {"status": "success", "contact_id": contact_id}

        kafka_produce('contact-updated-topic', {
            'id': contact_id,
            'first_name': event.first_name,
            'last_name': event.last_name,
            'email': event.email
        })
        return {"status": "success", "contact_id": contact_id}
    except Exception as e:
        logging.error(f"Error updating contact: {e}")
        raise HTTPException(status_code=500, detail="Error updating contact")

@app.post("/contact")
async def create_contact(event: CustomerEvent):
    sf = get_salesforce_instance()
    try:
        # Create new contact in Salesforce
        new_contact = sf.Contact.create({
            'FirstName': event.first_name,
            'LastName': event.last_name,
            'Email': event.email
        })
        return {"status": "success", "contact_id": new_contact['id']}
    except Exception as e:
        logging.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail="Error creating contact")



@app.get("/contacts/soql")
async def get_contacts_soql(last_name: Optional[str] = Query(None, description="The last name to search for")) -> List[dict]:
    sf = get_salesforce_instance()
    results = []
    try:
        if last_name:
            # Perform SOQL query
            query = f"SELECT Id, FirstName, LastName, Email FROM Contact WHERE LastName = '{last_name}'"
            # Use query_all_iter to handle large result sets
            for row in sf.query_all_iter(query):
                results.append(row)
            return results
        else:
            return {"status": "error", "message": "No last name provided"}
    except Exception as e:
        logging.error(f"Error performing SOQL query: {e}")
        raise HTTPException(status_code=500, detail="Error performing SOQL query")