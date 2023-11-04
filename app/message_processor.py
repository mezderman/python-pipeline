import os, tempfile, json, hashlib, sys
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.auto import partition

from app.shared.azure_service import AzureService
# from azure.storage.blob import BlobServiceClient, ContainerClient


def process_message_data(message_json):
    container_name = message_json['blobContainerName']
    blob_name = message_json['blobName']
    mime_type = message_json['mimeType']

    azure_service= AzureService()

    #check if this file was already processed
    content_hash = hashlib.md5(blob_name.encode()).hexdigest()
    filename = f"{content_hash}.json"
    embeddings_blob_client = azure_service.get_blob_client('embeddings', filename)

    # process only new files
    if not azure_service.blob_exists(embeddings_blob_client):
        blob_client = azure_service.get_blob_client(container_name, blob_name)
        
        props = blob_client.get_blob_properties()
        # content_type = props['content_settings']['content_type'] #mime_type
        temp_path = None  # Initialize temp_path to None
        
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                blob_data = blob_client.download_blob()
                temp.write(blob_data.readall())
                temp_path = temp.name
          
        except Exception as e:
            print(f"Error occurred: {e}")
            return f"Error occurred: {e}"  # Return early if there's an error
        
        # This will only be reached if temp_path is assigned a value
        if temp_path and os.path.exists(temp_path):
            
            elements = partition(filename=temp_path, content_type=mime_type)

            # TODO decide what content we’d like to keep
                
            print("\n\n".join([str(el) for el in elements][:10]))



    

   