import os
from azure.storage.queue import QueueClient
from app.shared.azure_queue_message import AzureQueueMessage
from app.shared.azure_service import AzureService

class QueueService:

    
    def __init__(self):
        print('init AzureQueueService')
        self.connection_string = os.getenv('AzureWebJobsStorage', 'default_value_if_not_set')
        self.azure_service = AzureService()

    def send_chunks_message(self, blob_name, chunk_blob_size_bytes):
        queue_name = 'chunks-processing-queue'
        

        # Create your message
        message_body = {'blobContainerName':'chunks','blobName':blob_name,'byteLength':chunk_blob_size_bytes, 'mimeType':'application/json', 'title':'place holder'}
        custom_metadata = {}
        message = AzureQueueMessage(message_text=message_body, custom_metadata=custom_metadata)

        # Send the message to the queue
        chunks_queue_client = self.azure_service.get_chunks_processing_queue()
        chunks_queue_client.send_message(message.to_json())

        return True
    
    
