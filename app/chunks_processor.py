# Standard library imports
import os, tempfile, json, hashlib, sys

# Related third party imports
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title

# Local application/library specific imports
from app.shared.azure_service import AzureService
from app.shared.composite_element_decoder import CompositeElementEncoder
from app.shared.queue_service import QueueService


queue_service = QueueService()

def process_message_data(message_json):
    container_name = message_json['blobContainerName']
    blob_name = message_json['blobName']
    mime_type = message_json['mimeType']

    azure_service= AzureService()

    #check if this file was already processed
    content_hash = hashlib.md5(blob_name.encode()).hexdigest()
    filename = f"{content_hash}.json"
    chunks_blob_client = azure_service.get_blob_client('chunks', filename)

    
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

        #chunk doc
        chunks = chunk_by_title(elements)
            
        # for chunk in chunks:
        #     print(chunk)
        #     print("\n\n" + "-"*80)

        serialized = json.dumps(chunks, cls=CompositeElementEncoder)
        serialized_json = json.loads(serialized)
        
        #update upstream event
        chunks_blob_client.upload_blob(serialized, overwrite=True)

        # Get blob properties
        chunks_blob_properties = chunks_blob_client.get_blob_properties()

        # Size of the blob in bytes
        chunk_blob_size_bytes = chunks_blob_properties.size

        queue_service.send_chunks_message(filename, chunk_blob_size_bytes)

    

   