
from azure.storage.blob import BlobServiceClient
from settings import *

def main():
    # Access a container using connection string
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Create container if it doesn't exist
    try:
        blob_service_client.create_container(CONTAINER_NAME)
    except:
        pass

    # Upload 5 blobs into the container
    for i in range(5):
        blob_name = f'sample-blob-{i}'
        blob_content = b'This is sample content to be encrypted.'

        upload_blob(blob_content, blob_service_client, CONTAINER_NAME, blob_name)


def upload_blob(
        data: bytes,
        blob_service_client: BlobServiceClient,
        container_name: str,
        blob_name: str) -> None:

    # Upload encrypted content to Azure storage
    kek = KeyWrapper(LOCAL_KEY_NAME, LOCAL_KEY_VALUE)

    # Access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.require_encryption = True
    blob_client.key_encryption_key = kek
    blob_client.encryption_version = '1.0'

    print(f"Uploading blob {blob_name} to Azure Storage...")

    blob_client.upload_blob(data, overwrite=OVERWRITE_EXISTING)


if __name__ == "__main__":
    main()
