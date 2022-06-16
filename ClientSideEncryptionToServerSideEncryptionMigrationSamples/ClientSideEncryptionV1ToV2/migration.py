
import os
from json import loads

from azure.storage.blob import BlobProperties, BlobServiceClient
from settings import *


def main():
    # Use connection string to access client account
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Ensure the container exists
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    if not container_client.exists():
        raise ValueError("The specified container does not exist.")

    # Loop through all blobs in the container
    for blob in container_client.list_blobs(include=['metadata']):
        # Determine if the blob is encrypted using client-side encryption V1
        if is_client_side_encrypted_v1(blob):
            # Migrate the blob from encryption V1 to V2
            migrate_blob_encryption(blob_service_client, CONTAINER_NAME, blob.name)


def is_client_side_encrypted_v1(blob: BlobProperties) -> bool:
    metadata = blob.metadata
    # Check for presence of encryption metadata
    if metadata and 'encryptiondata' in metadata:
        try:
            # Parse the encryption data to find version
            encryption_data = loads(metadata['encryptiondata'])
            if encryption_data['EncryptionAgent']['Protocol'] == '1.0':
                return True

        except (ValueError, KeyError):
            return False

    return False


def migrate_blob_encryption(
        blob_service_client: BlobServiceClient, 
        container_name: str,
        blob_name: str) -> None:

    kek = KeyWrapper(LOCAL_KEY_NAME, LOCAL_KEY_VALUE)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.require_encryption = True
    blob_client.key_encryption_key = kek

    print(f"\nReading blob {blob_name} from Azure Storage...")
    # Write decrypted contents of blob to a file
    with open("decryptedcontentfile.txt", "wb") as stream:
        blob_client.download_blob().readinto(stream)

    # Determine new blob name based on settings
    if not OVERWRITE_EXISTING:
        blob_name = blob_name + NEW_BLOB_SUFFIX

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.require_encryption = True
    blob_client.key_encryption_key = kek
    blob_client.encryption_version = '2.0'  # Use Version 2.0!

    print(f"Writing blob {blob_name} back to Azure Storage...")
    # Re-upload the blob using encryption V2
    with open("decryptedcontentfile.txt", "rb") as stream:
        blob_client.upload_blob(stream, overwrite=OVERWRITE_EXISTING)

    # Clean up temporary file
    os.remove("decryptedcontentfile.txt")


if __name__ == '__main__':
    main()
