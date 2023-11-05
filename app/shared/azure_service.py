from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueClient
import os

#Singleton
class AzureService:

    _instance = None
    _is_initialized = False

    _connection_string = None
    _blob_service_client = None
    _docs_processing_queue_client = None
    _chunks_processing_queue_client = None

    

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AzureService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not self._is_initialized:
            print("init Azure Services")
            self._connection_string = os.getenv('AzureWebJobsStorage', 'default_value_if_not_set')
            self._blob_service_client = BlobServiceClient.from_connection_string(self._connection_string)
            self._docs_processing_queue_client = QueueClient.from_connection_string(self._connection_string, "docs-processing-queue")
            self._chunks_processing_queue_client = QueueClient.from_connection_string(self._connection_string, "chunks-processing-queue")
            self._is_initialized = True

    def get_blob_client(self,container_name, blob_name):
        container_client = self._blob_service_client.get_container_client(container_name)
        return container_client.get_blob_client(blob_name)
    
    def get_chunks_processing_queue(self):
        return self._chunks_processing_queue_client
    
    def get_docs_processing_queue(self):
        return self._chunks_processing_queue_client
    
    def blob_exists(self, client):
        try:
            client.get_blob_properties()
            return True
        except:
            return False
