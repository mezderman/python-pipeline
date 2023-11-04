import azure.functions as func
from azure.storage.blob import BlobServiceClient, ContainerClient
import logging,sys,json
from pathlib import Path
from app.message_processor import process_message_data

# Ensure that the directory containing shared code is on the Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

app = func.FunctionApp()

@app.queue_trigger(arg_name="azqueue", queue_name="myqueue",
                               connection="QueueConnectionString") 
def queue_trigger(azqueue: func.QueueMessage):
    logging.info('Python Queue trigger processed a message: %s',
                azqueue.get_body().decode('utf-8'))
    
    message_str = azqueue.get_body().decode('utf-8')

    try:
        message_json = json.loads(message_str)
        process_message_data(message_json['messageText'])
    except json.JSONDecodeError as e:
        print("The message could not be converted to JSON:", e)
