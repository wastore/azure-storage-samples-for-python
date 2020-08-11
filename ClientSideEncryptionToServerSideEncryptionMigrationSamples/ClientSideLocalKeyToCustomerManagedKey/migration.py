from ClientSideEncryptionToServerSideEncryptionMigrationSamples.ClientSideLocalKeyToCustomerManagedKey.settings import *
from azure.storage.blob import BlobServiceClient
from azure.keyvault.keys import KeyClient
from azure.identity import ClientSecretCredential
import os


def main():
    # use connection string to access client account
    bs_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    key_client = KeyClient(vault_url=KEYVAULT_URL, credential=credentials)

    # create encryption scope
    if CREATE_ENCRYPTION_SCOPE:
        key_uri = get_key_uri(key_client)
        create_encryption_scope(key_uri)

    # call to run methods
    download_blob(BLOB_NAME, bs_client, CONTAINER_NAME)
    upload_blob(BLOB_NAME, bs_client, CONTAINER_NAME)


def get_key_uri(k_client):
    # this method gets a customer managed keyvault key to make encryption scope for server side encryption
    keyvault_key = k_client.get_key(SERVER_SIDE_KEYNAME)
    # get key_uri for encryption scope
    k_uri = str(keyvault_key.id)

    return k_uri


def create_encryption_scope(k_uri):
    print("\nCreating Customer Managed Key Encryption Scope...\n")
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + STORAGE_ACCOUNT + ' --name ' + CUSTOMER_MANAGED_ENCRYPTION_SCOPE + ' --key-source Microsoft.KeyVault --resource-group ' + RESOURCE_GROUP + ' --subscription ' + SUBSCRIPTION_ID + ' --key-uri ' + k_uri + '"')


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
        blob_client.upload_blob(stream, encryption_scope=CUSTOMER_MANAGED_ENCRYPTION_SCOPE, blob_type=blobtype,
                                overwrite=OVERWRITER)

    print("\nBlob uploaded to Azure Storage Account.")

    os.remove("decryptedcontentfile.txt")


if __name__ == '__main__':
    main()
