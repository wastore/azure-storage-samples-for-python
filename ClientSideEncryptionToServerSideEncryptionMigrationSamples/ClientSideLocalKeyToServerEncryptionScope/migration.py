
import os
from json import loads

from azure.storage.blob import BlobProperties, BlobServiceClient, BlobType
from settings import *


def main():
    # Use connection string to access client account
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    # Ensure the container exists
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    if not container_client.exists():
        raise ValueError("The specified container does not exist.")

    # Create encryption scope if needed
    if CREATE_ENCRYPTION_SCOPE:
        create_encryption_scope()

    # Loop through all blobs in the container
    for blob in container_client.list_blobs(include=['metadata']):
        # Determine if the blob is encrypted using client-side encryption V1
        if is_client_side_encrypted_v1(blob):
            # Download and decrypt blob to file
            download_blob(blob_service_client, CONTAINER_NAME, blob.name)
            # Upload server-side encrypted blob
            upload_blob(blob_service_client, CONTAINER_NAME, blob.name, blob.blob_type)


def create_encryption_scope() -> None:
    # If a KeyVault URI was specified, create a Customer managed Encryption Scope 
    if ENCRYPTION_SCOPE_KEY_KEYVAULT_URI:
        print("\nCreating Customer Managed Key Encryption Scope...\n")
        os.system(
            'cmd /c "az storage account encryption-scope create --account-name ' + STORAGE_ACCOUNT + ' --name ' + ENCRYPTION_SCOPE_NAME + ' --key-source Microsoft.KeyVault --resource-group ' + RESOURCE_GROUP + ' --subscription ' + SUBSCRIPTION_ID + ' --key-uri ' + k_uri + '"')

    # Else create a Microsoft managed Encryption Scope
    else:
        print("\nCreating Microsoft Managed Key Encryption Scope...\n")
        os.system(
            'cmd /c "az storage account encryption-scope create --account-name ' + STORAGE_ACCOUNT + ' --name ' + ENCRYPTION_SCOPE_NAME + ' --key-source Microsoft.Storage --resource-group ' + RESOURCE_GROUP + ' --subscription ' + SUBSCRIPTION_ID + '"')


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


def download_blob(
        blob_service_client: BlobServiceClient, 
        container_name: str,
        blob_name: str) -> None:
    # Download encrypted blob from azure storage
    kek = KeyWrapper(LOCAL_KEY_NAME, LOCAL_KEY_VALUE)
    # Access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.key_encryption_key = kek

    print(f"\nReading blob {blob_name} from Azure Storage...")
    # Write decrypted contents of blob to a file
    with open("decryptedcontentfile.txt", "wb") as stream:
        blob_client.download_blob().readinto(stream)


def upload_blob(
        blob_service_client: BlobServiceClient,
        container_name: str,
        blob_name: str,
        blob_type: BlobType) -> None:

    print("Performing server-side encryption with an Encryption Scope...")

    # Determine blob name based on settings
    if not OVERWRITE_EXISTING:
        blob_name = blob_name + NEW_BLOB_SUFFIX

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open("decryptedcontentfile.txt", "rb") as stream:
        blob_client.upload_blob(
            stream,
            encryption_scope=ENCRYPTION_SCOPE_NAME,
            blob_type=blob_type,
            overwrite=OVERWRITE_EXISTING)

    print(f"Blob {blob_name} uploaded to Azure Storage Account.")

    # Clean up temporary file
    os.remove("decryptedcontentfile.txt")


if __name__ == '__main__':
    main()
