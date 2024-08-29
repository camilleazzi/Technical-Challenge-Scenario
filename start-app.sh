#!/bin/bash

#!/bin/bash

# Navigate to the pub-sub-api/python directory
cd "$(dirname "$0")"

# Start the FastAPI application using Uvicorn
uvicorn main:app --reload &


# Wait for the server to start
sleep 2

# Open the API documentation in the default web browser
open http://127.0.0.1:8000/docs

# Display server information
echo "INFO:     Will watch for changes in these directories: [$(pwd)]"
echo "INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"
echo "INFO:     Started reloader process using StatReload"

# Run the PubSubAPIClient script
cd pub-sub-api/python
python3 PubSubApiClient.py






