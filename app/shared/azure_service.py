import os
from azure.storage.blob import BlobServiceClient

class AzureService:

    connection_string = None
    blob_service_client = None
    
    def __init__(self):
        print("init Azure Services")
        
        self.connection_string = os.getenv('AzureWebJobsStorage', 'default_value_if_not_set')
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def get_blob_client(self,container_name, blob_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        return container_client.get_blob_client(blob_name)
    
    def blob_exists(self, client):
        try:
            client.get_blob_properties()
            return True
        except:
            return False
