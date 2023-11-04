import os,uuid,json
from datetime import datetime, timedelta
from azure.storage.queue import QueueClient
from app.shared.azure_queue_message import AzureQueueMessage

class QueueService:

    
    def __init__(self):
        print('init AzureQueueService')
        self.connection_string = os.getenv('AzureWebJobsStorage', 'default_value_if_not_set')

    def send_chunks_message(self, blob_name, chunk_blob_size_bytes):
        queue_name = 'chunks-processing-queue'

        # Instantiate a QueueClient which will be used to create and send messages
        queue_client = QueueClient.from_connection_string(self.connection_string, queue_name)

        # Create your message
        message_body = {'blobContainerName':'chunks','blobName':blob_name,'byteLength':chunk_blob_size_bytes, 'mimeType':'application/json', 'title':'place holder'}
        custom_metadata = {}
        message = AzureQueueMessage(message_text=message_body, custom_metadata=custom_metadata)

        # Send the message to the queue
        queue_client.send_message(message.to_json())

        return True
    
    
