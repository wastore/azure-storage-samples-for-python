import os
from azure.storage.blob import BlobServiceClient
from ClientSideLocalKeyToMicrosoftManagedKey.settings import *


def main():
    # use connection string to access client account
    bs_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    # access your container-- this container must already exist to run this program
    bs_client.get_container_client(CONTAINER_NAME)

    # create encryption scope
    if CREATE_ENCRYPTION_SCOPE:
        create_encryption_scope()

    # call to run methods
    download_blob(BLOB_NAME, bs_client, CONTAINER_NAME)
    upload_blob(BLOB_NAME, bs_client, CONTAINER_NAME)


def create_encryption_scope():
    print("\nCreating Microsoft Managed Key Encryption Scope...\n")
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + STORAGE_ACCOUNT + ' --name ' + SERVER_MANAGED_ENCRYPTION_SCOPE + ' --key-source Microsoft.Storage --resource-group ' + RESOURCE_GROUP + ' --subscription ' + SUBSCRIPTION_ID + '"')


def download_blob(filename, blob_service_client, cont_name):
    # download encrypted blob from azure storage
    kek = KeyWrapper(LOCAL_KEY_VALUE)
    # access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    blob_client.key_encryption_key = kek
    print("\nReading blob from Azure Storage...")
    # write encrypted contents of blob to a file
    with open("decryptedcontentfile.txt", "wb+") as stream:
        blob_client.download_blob().readinto(stream)


def upload_blob(filename, blob_service_client, cont_name):
    # upload decrypted blob back to azure storage and perform server side encryption

    # determine the blob type for upload
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    properties = blob_client.get_blob_properties()
    blobtype = properties.blob_type

    # upload and use server side encryption with Microsoft managed key through encryption scope
    print("\nPerforming server side encryption with Microsoft Managed Key Encryption Scope...")
    # access specific container and blob
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=MIGRATED_BLOB_NAME)
    # upload and perform server side encryption with Microsoft managed encryption scope
    with open("decryptedcontentfile.txt", "rb") as stream:
        blob_client.upload_blob(stream, encryption_scope=SERVER_MANAGED_ENCRYPTION_SCOPE, blob_type=blobtype, overwrite=OVERWRITER)

    print("\nBlob uploaded to Azure Storage Account.")

    os.remove("decryptedcontentfile.txt")


if __name__ == '__main__':
    main()
