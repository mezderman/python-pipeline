import json, uuid
from datetime import datetime, timedelta
import os

# Assuming the schema is for your internal use and not for direct Azure Queue attributes
class AzureQueueMessage:
    def __init__(self, message_text, custom_metadata=None):
        self.messageId = str(uuid.uuid4())
        self.insertionTime = datetime.utcnow()
        self.expirationTime = self.insertionTime + timedelta(days=7)  # Example: 7 days expiration
        self.dequeueCount = 0  # This will be 0 initially
        self.nextVisibleTime = self.insertionTime  # Initially, it will be visible immediately
        self.popReceipt = ""  # This will be filled by Azure Queue after the message is enqueued
        self.messageText = message_text
        self.customMetadata = custom_metadata if custom_metadata else {}

    def to_json(self):
        # Convert to dict and then to JSON string, also format dates to ISO string
        message_dict = {
            "messageId": self.messageId,
            "insertionTime": self.insertionTime.isoformat(),
            "expirationTime": self.expirationTime.isoformat(),
            "dequeueCount": self.dequeueCount,
            "nextVisibleTime": self.nextVisibleTime.isoformat(),
            "popReceipt": self.popReceipt,
            "messageText": self.messageText,
            "customMetadata": self.customMetadata,
        }
        return json.dumps(message_dict)


