from azure.storage.blob import BlobServiceClient
from ClientSideEncryptionToServerSideEncryptionMigrationSamples.ClientSideLocalKeyToMicrosoftManagedKey.settings import *


def main():
    # access a container using connection string
    bs_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # create container by name
    try:
        bs_client.create_container(CONTAINER_NAME)
    except:
        bs_client.get_container_client(CONTAINER_NAME)

    # call to methods
    content = get_content(BLOB_NAME)
    upload_blob(content, bs_client, CONTAINER_NAME, BLOB_NAME)


def get_content(filename):
    file_content = open(filename, "rb+")
    data = file_content.read()

    return data


def upload_blob(data, blob_service_client, container_name, b_name):
    # upload encrypted content to Azure storage
    kek = KeyWrapper(LOCAL_KEY_VALUE)

    # access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=b_name)
    blob_client.key_encryption_key = kek

    print("\nUploading blob to Azure Storage...")
    print("\nEncrypting blob on server...")

    blob_client.upload_blob(data, overwrite=OVERWRITER)


if __name__ == "__main__":
    main()
